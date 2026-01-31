DELETE FROM event e
WHERE NOT EXISTS (
  SELECT 1
  FROM ticket t
  WHERE t.ecode = e.ecode
  AND NOT EXISTS (
    SELECT 1 FROM cancel c WHERE c.tno = t.tno
  )
);


DELETE FROM spectator s
WHERE NOT EXISTS (
  SELECT 1
  FROM ticket t
  WHERE t.sno = s.sno
  AND NOT EXISTS (
    SELECT 1 FROM cancel c WHERE c.tno = t.tno
  )
);
INSERT INTO ticket (tno, ecode, sno)
SELECT 003, 'E002', 003
WHERE NOT EXISTS (]
    SELECT 1
    FROM ticket
    WHERE ecode = 'E002'
      AND sno = 003
);

SELECT 
  e.elocation,
  e.edate,
  COUNT(DISTINCT t.sno) AS total_spectators
FROM event e
JOIN ticket t ON t.ecode = e.ecode
LEFT JOIN cancel c ON c.tno = t.tno
WHERE c.tno IS NULL
GROUP BY e.elocation, e.edate;

SELECT 
  e.edesc,
  COUNT(t.tno) AS total_tickets
FROM event e
LEFT JOIN ticket t ON t.ecode = e.ecode
GROUP BY e.edesc
ORDER BY e.edesc;

SELECT 
  e.edesc,
  COUNT(t.tno) AS total_tickets
FROM event e
LEFT JOIN ticket t ON t.ecode = e.ecode
WHERE e.ecode = 'E002'
GROUP BY e.edesc;

SELECT 
  s.sname,
  e.edate,
  e.elocation,
  e.etime,
  e.edesc
FROM spectator s
JOIN ticket t ON t.sno = s.sno
JOIN event e ON e.ecode = t.ecode
LEFT JOIN cancel c ON c.tno = t.tno
WHERE s.sno = 002
AND c.tno IS NULL;

SELECT 
  s.sname,
  t.ecode,
  CASE 
    WHEN c.tno IS NULL THEN 'VALID'
    ELSE 'CANCELLED'
  END AS ticket_status
FROM ticket t
JOIN spectator s ON s.sno = t.sno
LEFT JOIN cancel c ON c.tno = t.tno
WHERE t.tno = 001;
SELECT 
  s.sname,
  t.ecode,
  CASE 
    WHEN c.tno IS NULL THEN 'VALID'
    ELSE 'CANCELLED'
  END AS ticket_status
FROM ticket t
JOIN spectator s ON s.sno = t.sno
LEFT JOIN cancel c ON c.tno = t.tno
WHERE t.tno = 001;

SELECT 
  c.tno,
  s.sname,
  e.edesc,
  c.cdate,
  c.cuser
FROM cancel c
JOIN ticket t ON t.tno = c.tno
JOIN spectator s ON s.sno = c.sno
JOIN event e ON e.ecode = c.ecode
WHERE c.ecode = 'E002';
SELECT 
  c.tno,
  s.sname,
  e.edesc,
  c.cdate,
  c.cuser
FROM cancel c
JOIN ticket t ON t.tno = c.tno
JOIN spectator s ON s.sno = c.sno
JOIN event e ON e.ecode = c.ecode
WHERE c.ecode = 'E002';