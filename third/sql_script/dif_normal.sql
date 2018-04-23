
SET search_path=public,pg_catalog;

-- [ Dropped objects ] --
ALTER TABLE public.tweet DROP COLUMN IF EXISTS name CASCADE;
-- ddl-end --
ALTER TABLE public.tweet DROP COLUMN IF EXISTS country_code CASCADE;
-- ddl-end --
ALTER TABLE public.tweet DROP COLUMN IF EXISTS lang CASCADE;
-- ddl-end --
ALTER TABLE public.tweet DROP COLUMN IF EXISTS location CASCADE;
-- ddl-end --


-- [ Created objects ] --
-- object: idtweet | type: COLUMN --
-- ALTER TABLE public.tweet DROP COLUMN IF EXISTS idtweet CASCADE;
ALTER TABLE public.tweet ADD COLUMN idtweet bigint NOT NULL;
-- ddl-end --


-- object: idtweetuser | type: COLUMN --
-- ALTER TABLE public.tweet DROP COLUMN IF EXISTS idtweetuser CASCADE;
ALTER TABLE public.tweet ADD COLUMN idtweetuser bigint;
-- ddl-end --


-- object: idcountry | type: COLUMN --
-- ALTER TABLE public.tweet DROP COLUMN IF EXISTS idcountry CASCADE;
ALTER TABLE public.tweet ADD COLUMN idcountry integer;
-- ddl-end --


-- object: idlang | type: COLUMN --
-- ALTER TABLE public.tweet DROP COLUMN IF EXISTS idlang CASCADE;
ALTER TABLE public.tweet ADD COLUMN idlang integer;
-- ddl-end --


-- object: public.tweetuser | type: TABLE --
-- DROP TABLE IF EXISTS public.tweetuser CASCADE;
CREATE TABLE public.tweetuser(
	idtweetuser bigint NOT NULL,
	idlang integer,
	idlocation integer,
	nameuser text,
	CONSTRAINT pk_tweetuser PRIMARY KEY (idtweetuser)

);
-- ddl-end --
ALTER TABLE public.tweetuser OWNER TO postgres;
-- ddl-end --

-- object: public.country | type: TABLE --
-- DROP TABLE IF EXISTS public.country CASCADE;
CREATE TABLE public.country(
	idcountry serial NOT NULL,
	countrycode text,
	CONSTRAINT pk_country PRIMARY KEY (idcountry)

);
-- ddl-end --
ALTER TABLE public.country OWNER TO postgres;
-- ddl-end --

-- object: public.lang | type: TABLE --
-- DROP TABLE IF EXISTS public.lang CASCADE;
CREATE TABLE public.lang(
	idlang serial NOT NULL,
	snamelang text,
	CONSTRAINT pk_lang PRIMARY KEY (idlang)

);
-- ddl-end --
ALTER TABLE public.lang OWNER TO postgres;
-- ddl-end --

-- object: tweetsentiment | type: COLUMN --
-- ALTER TABLE public.tweet DROP COLUMN IF EXISTS tweetsentiment CASCADE;
ALTER TABLE public.tweet ADD COLUMN tweetsentiment bigint;
-- ddl-end --


-- object: public.location | type: TABLE --
-- DROP TABLE IF EXISTS public.location CASCADE;
CREATE TABLE public.location(
	idlocation serial NOT NULL,
	namelocation text,
	CONSTRAINT pk_location PRIMARY KEY (idlocation)

);
-- ddl-end --
ALTER TABLE public.location OWNER TO postgres;
-- ddl-end --



-- [ Created constraints ] --
-- object: pk_tweet | type: CONSTRAINT --
-- ALTER TABLE public.tweet DROP CONSTRAINT IF EXISTS pk_tweet CASCADE;
ALTER TABLE public.tweet ADD CONSTRAINT pk_tweet PRIMARY KEY (idtweet);
-- ddl-end --



-- [ Created foreign keys ] --
-- object: fk_tweet_tweetuser | type: CONSTRAINT --
-- ALTER TABLE public.tweet DROP CONSTRAINT IF EXISTS fk_tweet_tweetuser CASCADE;
ALTER TABLE public.tweet ADD CONSTRAINT fk_tweet_tweetuser FOREIGN KEY (idtweetuser)
REFERENCES public.tweetuser (idtweetuser) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: fk_tweet_country | type: CONSTRAINT --
-- ALTER TABLE public.tweet DROP CONSTRAINT IF EXISTS fk_tweet_country CASCADE;
ALTER TABLE public.tweet ADD CONSTRAINT fk_tweet_country FOREIGN KEY (idcountry)
REFERENCES public.country (idcountry) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: fk_tweet_lang | type: CONSTRAINT --
-- ALTER TABLE public.tweet DROP CONSTRAINT IF EXISTS fk_tweet_lang CASCADE;
ALTER TABLE public.tweet ADD CONSTRAINT fk_tweet_lang FOREIGN KEY (idlang)
REFERENCES public.lang (idlang) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: fk_tweetuser_lang | type: CONSTRAINT --
-- ALTER TABLE public.tweetuser DROP CONSTRAINT IF EXISTS fk_tweetuser_lang CASCADE;
ALTER TABLE public.tweetuser ADD CONSTRAINT fk_tweetuser_lang FOREIGN KEY (idlang)
REFERENCES public.lang (idlang) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: fk_tweetuser_location | type: CONSTRAINT --
-- ALTER TABLE public.tweetuser DROP CONSTRAINT IF EXISTS fk_tweetuser_location CASCADE;
ALTER TABLE public.tweetuser ADD CONSTRAINT fk_tweetuser_location FOREIGN KEY (idlocation)
REFERENCES public.location (idlocation) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

