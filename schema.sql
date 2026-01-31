CREATE TABLE event (
    ecode        CHAR(4) Primary key,
    edesc        VARCHAR(20),
    elocation    VARCHAR(20),
    edate        DATE check(edate between date '2026-07-01' and date '2026-07-31'),
    etime        TIME check(etime >= time '09:00'),
    emax         SMALLINT check(emax between 1 and 1000));

CREATE TABLE spectator (
    sno          INTEGER primary key,
    sname        VARCHAR(20),
    semail       VARCHAR(20) );

CREATE TABLE ticket (
    tno          INTEGER Primary key,
    ecode        CHAR(4) REFERENCES event(ecode),
    sno          INTEGER REFERENCES spectator(sno) );

CREATE TABLE cancel (
    tno          INTEGER references  ticket(tno) primary key,
    ecode        CHAR(4) references event(ecode),
    sno          INTEGER references spectator(sno),
    cdate        TIMESTAMP,
    cuser        VARCHAR(128));