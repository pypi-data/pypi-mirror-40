from dataclasses import dataclass
from typing import List, Set, Optional, Tuple
import datetime
import bs4
import requests
from itertools import zip_longest
from mashumaro import DataClassJSONMixin


__all__ = ["Substitution", "SubstitutionTable", "substitutiontables_from_urls"]


@dataclass(frozen=True)
class Substitution(DataClassJSONMixin):
    classes: Tuple[str]
    period: str
    subject_new: str
    subject_old: str
    teacher_new: str
    teacher_old: str
    room: str
    type: str
    text: str

    def pretty(self) -> str:
        text = ""

        if self.type == "Ausfall":
            text += "{period}. Stunde: {subject_old} "
            if self.teacher_old != "":
                text += "bei {teacher_old} "
            text += "entfällt"
            if self.text != "":
                text += "{text}"
        elif self.type == "Raum-Vtr.":
            if self.teacher_new == self.teacher_old:
                text += "{period}. Stunde: {subject_new} bei {teacher_old} verlegt zu Raum {room}"
            else:
                text += "{period}. Stunde: {subject_new} bei {teacher_old} verlegt zu Raum {room} bei {teacher_new}"
        elif self.type == "Vertretung":
            text += "{period}. Stunde "
            if self.subject_new != "" and self.subject_old != "":
                if self.teacher_new == "+":
                    text += "{subject_old} in Raum {room} entfällt"
                else:
                    text += "{subject_old} Vertretung bei {teacher_new} statt {teacher_old} in Raum {room}"
            elif self.subject_new != "" and self.subject_old == "":
                text += "Klausur: {text}"
            else:
                if self.teacher_new == "+":
                    text += "{subject_old} entfällt"
                else:
                    text += "{subject_old} Vertretung bei {teacher_new}"
        elif self.type == "Verlegung":
            text += "{period}. Stunde: {subject_new} bei {teacher_new} anstelle von {subject_old} bei {teacher_old}; {subject_old} verlegt auf {text}"
        elif self.type == "Freistunde":
            text += "{period}. Stunde: {subject_old} bei {teacher_old} fällt aus"
        elif self.type == "Tausch":
            if (
                self.teacher_new == self.teacher_old
                and self.subject_new == self.subject_old
            ):
                text += "{period}. Stunde {subject_new} bei {teacher_old}: {text}"
            else:
                text += "{period}. Stunde {subject_old} bei {teacher_old} getauscht mit {subject_new} bei {teacher_new}: {text}"
        elif self.type == "Sondereinsatz":
            text += "{period}. Stunde: Sondereinsatz in Raum {room}"
        elif self.type == "Betreuung":
            text += "{period}. Stunde: Betreuung durch {teacher_new} in Raum {room}"
        elif self.type == "Pausenaufsicht":
            if self.teacher_new == "???" and self.teacher_old != "":
                text += "Pausenaufsicht von {teacher_old} auf {room} in der {period}"
            else:
                text += "Pausenaufsicht von {teacher_new} auf {room} in der {period}"
        else:
            text += "TODO: {type}. pls contact fijitech"

        return text.format(
            period=self.period,
            subject_new=self.subject_new,
            subject_old=self.subject_old,
            teacher_new=self.teacher_new,
            teacher_old=self.teacher_old,
            room=self.room,
            type=self.type,
            text=self.text,
        )


@dataclass
class SubstitutionTable(DataClassJSONMixin):
    affected: Set[str]
    absent: Set[str]
    substitutions: List[Substitution]
    date: datetime.date


def _parse_substitution_table(
    date_element: bs4.element.Tag,
    additional_info: Optional[bs4.element.Tag],
    substitution_table: Optional[bs4.element.Tag],
) -> SubstitutionTable:
    date = datetime.datetime.strptime(
        date_element.text.split(", ")[0], "%d.%m.%Y"
    ).date()

    affected = []  # type: List[str]
    absent = []  # type: List[str]
    if additional_info is not None:
        for tr in additional_info.findAll("tr"):
            if tr.find("td") is not None:
                if "Betroffene" in tr.find("td").text:
                    affected = tr.findAll("td")[1].text.split(", ")
                elif "Abwesende" in tr.find("td").text:
                    absent = tr.findAll("td")[1].text.split(", ")

    subs = []  # type: List[Substitution]
    if substitution_table is not None:
        is_teacher_subs = (
            not substitution_table.find("tr", {"class": "TeacherHead"}) is None
        )

        for tr in substitution_table.findAll("tr"):
            if "TeacherHead" in tr.attrs["class"]:
                continue
            subData = [x.text for x in tr.findAll("td")]

            if is_teacher_subs:
                sub = Substitution(
                    tuple(subData[4].split(", ")),
                    subData[1],
                    subData[5],
                    subData[8],
                    subData[0],
                    subData[3],
                    subData[6],
                    subData[2],
                    subData[7],
                )
            else:
                sub = Substitution(
                    tuple(subData[0].split(", ")),
                    subData[1],
                    subData[2],
                    subData[3],
                    subData[4],
                    subData[5],
                    subData[6],
                    subData[8],
                    subData[9],
                )

            if sub not in subs:
                subs.append(sub)
        del subs[0]

    return SubstitutionTable(set(affected), set(absent), subs, date)


def _parse_substitutions_url(url) -> List[SubstitutionTable]:
    soup = bs4.BeautifulSoup(requests.get(url).content, "html.parser")

    # ignoriere alls h1, die Klasse "NoSubstitutes" sind
    # => überspringe "Keine Vertretungen"-Text
    dates = filter(
        lambda x: "NoSubstitutes" not in x.attrs.get("class", []), soup.findAll("h1")
    )
    addInfo = soup.findAll("table", {"class": "additionInfoTable"})
    subsTable = soup.findAll("table", attrs={"cellspacing": 1})

    return [
        _parse_substitution_table(*x) for x in zip_longest(dates, addInfo, subsTable)
    ]


def substitutiontables_from_urls(urls: List[str]) -> List[SubstitutionTable]:
    # die liste der Vertretungspläne, die am ende returt wird
    timetables = []  # type: List[SubstitutionTable]
    for url in urls:
        for new_timetable in _parse_substitutions_url(url):
            for old_timetable in timetables:
                # falls das datum bereits vorhanden ist, füge alten und neuen
                # Plan zusammen
                if new_timetable.date == old_timetable.date:
                    old_timetable.affected.update(new_timetable.affected)
                    old_timetable.absent.update(new_timetable.absent)
                    old_timetable.substitutions.extend(new_timetable.substitutions)
                    break
            else:
                # falls das datum noch nicht in der liste ist,
                # hänge Plan hinten an
                timetables.append(new_timetable)
    for timetable in timetables:
        timetable.substitutions = sorted(
            timetable.substitutions, key=lambda s: s.classes
        )
    return sorted(timetables, key=lambda t: t.date)
