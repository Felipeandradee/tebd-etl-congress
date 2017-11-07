import datetime

from dw_models import Autor as AutorDW, Year as YearDW, Congress as CongressDW, Admissions as AdmissionsDW
from models import Participant, Congress, Paper, Autor, Congress_Paper


def autor():
    all_participants = Participant.select(Participant.registrationId, Participant.name, Participant.workplace)
    for p in all_participants:
        AutorDW.get_or_create(idautor=p.registrationId, autorname=p.name, workplace=p.workplace)


def year():
    all_years = Congress.select(Congress.submissionDeadline.year.alias('year')).distinct()
    for id, y in enumerate(all_years, start=1):
        YearDW.get_or_create(idyear=id, congressyear=y.year)

rm 
def congress():
    all_congresses = Congress.select(Congress.idCongress, Congress.name)
    for c in all_congresses:
        CongressDW.get_or_create(idcongress=c.idCongress, congressname=c.name)


def admissions():
    all_years = YearDW.select()

    for y in all_years:
        all_congresses = Congress.select(Congress.idCongress) \
            .where(Congress.submissionDeadline.year == y.congressyear)
        for c in all_congresses:
            rel_congress_paper = Congress_Paper.select(Congress_Paper.idPaper) \
                .where(Congress_Paper.idCongress == c.idCongress)
            rel_congress = [r.idPaper for r in rel_congress_paper]
            autors_papers = [a.idParticipant for a in
                             Autor.select(Autor.idParticipant).where(Autor.idPaper << rel_congress)]
            all_autors = AutorDW.select(AutorDW.idautor).where(AutorDW.idautor << autors_papers)
            for l_autor in all_autors:
                rel_autor = [a.idPaper for a in Autor.select()
                    .where(Autor.idParticipant == l_autor.idautor, Autor.idPaper << rel_congress)]
                n_refused = Paper.select() \
                    .where(Paper.accepted == False,
                           Paper.paperId << rel_autor,
                           Paper.paperId << rel_congress) \
                    .count()
                n_accepted = Paper.select() \
                    .where(Paper.accepted,
                           Paper.paperId << rel_autor,
                           Paper.paperId << rel_congress) \
                    .count()

                if (n_refused + n_accepted) > 0:
                    AdmissionsDW.get_or_create(idadmcongress=c.idCongress, idadmautor=l_autor.idautor,
                                               accepted=n_accepted, refused=n_refused, idadmyear=y.idyear)
