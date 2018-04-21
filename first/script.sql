SELECT
  test.idsqltest    AS "id",
  test.valuesqltest AS "value",
  test.datesqltest  AS "date"
FROM
  (
    SELECT
      sqltest.idsqltest,
      sqltest.valuesqltest,
      sqltest.datesqltest,
      row_number() OVER (PARTITION BY sqltest.idsqltest ORDER BY sqltest.datesqltest DESC, sqltest.valuesqltest DESC) AS id_group
    FROM
      sqltest
  ) AS test
WHERE
  test.id_group = 1;