from main.models import *

#region Methods
def getAttendingStats(periodStart, periodEnd, union, group, student):
    allAttendings = [a
                     for a in Attending.objects.all()
                     if a.studySession.date.date() >= periodStart
                     and a.studySession.date.date() <= periodEnd
                     and (union is None or a.studySession.group.union.id == int(union))
                     and (group is None or a.studySession.group.id == int(group))
                     and (student is None or a.student.id == int(student))
                     ]

    attendedAttendings = [a
                          for a in allAttendings
                          if a.isAttend==True]

    if len(allAttendings) == 0: allAttendings = 1;
    else: allAttendings = len(allAttendings)
    return len(attendedAttendings) / allAttendings, len(attendedAttendings), allAttendings

def getGenderStats(union, group):
    allStudents = getAllStudents(union, group)
    maleStudents = [m
                    for m in allStudents
                    if m.gender == "Мужской"]

    return len(maleStudents) / len(allStudents), len(maleStudents), len(allStudents)

def getAgeStats(min, max, union, group):
    allStudents = getAllStudents(union, group)
    chosenStudents = [m
                      for m in allStudents
                      if m.age >= min
                      and m.age <= max]

    return len(chosenStudents) / len(allStudents), len(chosenStudents), len(allStudents)
#endregion

#region Methods for other methods
def getAllStudents(union, group):
    return [s
            for s in Student.objects.all()
            if (union is None or s.group.union.id == int(union))
            and (group is None or s.group.id == int(group))
            ]
#endregionings, len(attendedAttendings), allAttendings