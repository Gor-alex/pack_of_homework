WITH country_sentimant AS (
    SELECT
      sum(tweet.tweetsentiment) AS "tweet_sentimant",
      country.idcountry         AS "idcountry"
    FROM
      tweet
        JOIN country ON tweet.idcountry = country.idcountry
    GROUP BY
      country.idcountry
), min_country AS (
    SELECT
      sentimant.tweet_sentimant,
      country_1.countrycode as "name"
    FROM
      country_sentimant sentimant
        JOIN country country_1 ON sentimant.idcountry = country_1.idcountry
    WHERE
      country_1.countrycode IS NOT NULL AND country_1.countrycode != ''
    ORDER BY
      sentimant.tweet_sentimant ASC
    LIMIT 1
), max_country AS (
    SELECT
      sentimant.tweet_sentimant,
      country_1.countrycode as "name"
    FROM
      country_sentimant sentimant
        JOIN country country_1 ON sentimant.idcountry = country_1.idcountry
    WHERE
      country_1.countrycode IS NOT NULL AND country_1.countrycode != ''
    ORDER BY
      sentimant.tweet_sentimant DESC
    LIMIT 1
), user_sentimant AS (
    SELECT
      tweetuser.idtweetuser,
      sum(tweet.tweetsentiment) AS "tweet_sentimant"
    FROM
      tweetuser
        JOIN tweet ON tweet.idtweetuser = tweetuser.idtweetuser
    GROUP BY
      tweetuser.idtweetuser
), max_user AS (
    SELECT
      sentimant.tweet_sentimant,
      tweetuser.nameuser as "name"
    FROM
      user_sentimant sentimant
        JOIN tweetuser ON tweetuser.idtweetuser = sentimant.idtweetuser
    WHERE
      tweetuser.nameuser is not NULL AND tweetuser.nameuser != ''
    ORDER BY
      sentimant.tweet_sentimant DESC
    LIMIT 1
), min_user AS (
    SELECT
      sentimant.tweet_sentimant,
      tweetuser.nameuser as "name"
    FROM
      user_sentimant sentimant
        JOIN tweetuser ON tweetuser.idtweetuser = sentimant.idtweetuser
    WHERE
      tweetuser.nameuser is not NULL AND tweetuser.nameuser != ''
    ORDER BY
      sentimant.tweet_sentimant ASC
    LIMIT 1
), location_sentimant AS (
    SELECT
      sum(tweet.tweetsentiment) AS "tweet_sentimant",
      tweetuser.idlocation
    FROM
      tweetuser
        JOIN tweet ON tweet.idtweetuser = tweetuser.idtweetuser
    GROUP BY
      tweetuser.idlocation
), min_location AS (
    SELECT
      sentimant.tweet_sentimant,
      loc.namelocation as "name"
    FROM
      location_sentimant sentimant
        JOIN location loc ON loc.idlocation = sentimant.idlocation
    WHERE
      loc.namelocation is not NULL AND loc.namelocation != ''
    ORDER BY
      sentimant.tweet_sentimant ASC
    LIMIT 1
), max_location AS (
    SELECT
      sentimant.tweet_sentimant,
      loc.namelocation as "name"
    FROM
      location_sentimant sentimant
        JOIN location loc ON loc.idlocation = sentimant.idlocation
    WHERE
      loc.namelocation is not NULL AND loc.namelocation != ''
    ORDER BY
      sentimant.tweet_sentimant DESC
    LIMIT 1
)

SELECT
  *
FROM
  max_country
UNION ALL
SELECT
  *
FROM
  min_country
UNION ALL
SELECT
  *
FROM
  min_user
UNION ALL
SELECT
  *
FROM
  max_user
UNION ALL
SELECT
  *
FROM
  min_location
UNION ALL
SELECT
  *
FROM
  max_location;