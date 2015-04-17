--
-- PostgreSQL database dump
--

-- Dumped from database version 9.4.1
-- Dumped by pg_dump version 9.4.0
-- Started on 2015-04-17 14:35:12 COT

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- TOC entry 176 (class 3079 OID 11861)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2026 (class 0 OID 0)
-- Dependencies: 176
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 172 (class 1259 OID 25031)
-- Name: date_landsat; Type: TABLE; Schema: public; Owner: omar; Tablespace: 
--

CREATE TABLE date_landsat (
    id_landsat character varying NOT NULL,
    date date NOT NULL
);


ALTER TABLE date_landsat OWNER TO omar;

--
-- TOC entry 175 (class 1259 OID 25055)
-- Name: discarded; Type: TABLE; Schema: public; Owner: omar; Tablespace: 
--

CREATE TABLE discarded (
    id_landsat character varying NOT NULL,
    latitude double precision NOT NULL,
    longitude double precision NOT NULL,
    reason character varying NOT NULL
);


ALTER TABLE discarded OWNER TO omar;

--
-- TOC entry 174 (class 1259 OID 25047)
-- Name: radiance; Type: TABLE; Schema: public; Owner: omar; Tablespace: 
--

CREATE TABLE radiance (
    id_landsat character varying NOT NULL,
    latitude double precision NOT NULL,
    longitude double precision NOT NULL,
    band1 double precision NOT NULL,
    band2 double precision NOT NULL,
    band3 double precision NOT NULL,
    band4 double precision NOT NULL
);


ALTER TABLE radiance OWNER TO omar;

--
-- TOC entry 173 (class 1259 OID 25039)
-- Name: reflectance; Type: TABLE; Schema: public; Owner: omar; Tablespace: 
--

CREATE TABLE reflectance (
    id_landsat character varying NOT NULL,
    latitude double precision NOT NULL,
    longitude double precision NOT NULL,
    band1 double precision NOT NULL,
    band2 double precision NOT NULL,
    band3 double precision NOT NULL,
    band4 double precision NOT NULL,
    band5 double precision NOT NULL,
    band6 double precision NOT NULL,
    band7 double precision NOT NULL
);


ALTER TABLE reflectance OWNER TO omar;

--
-- TOC entry 1900 (class 2606 OID 25038)
-- Name: date_landsat_pk; Type: CONSTRAINT; Schema: public; Owner: omar; Tablespace: 
--

ALTER TABLE ONLY date_landsat
    ADD CONSTRAINT date_landsat_pk PRIMARY KEY (id_landsat);


--
-- TOC entry 1906 (class 2606 OID 25062)
-- Name: discarded_pk; Type: CONSTRAINT; Schema: public; Owner: omar; Tablespace: 
--

ALTER TABLE ONLY discarded
    ADD CONSTRAINT discarded_pk PRIMARY KEY (id_landsat, latitude, longitude);


--
-- TOC entry 1904 (class 2606 OID 25054)
-- Name: radiance_pk; Type: CONSTRAINT; Schema: public; Owner: omar; Tablespace: 
--

ALTER TABLE ONLY radiance
    ADD CONSTRAINT radiance_pk PRIMARY KEY (id_landsat, latitude, longitude);


--
-- TOC entry 1902 (class 2606 OID 25046)
-- Name: reflectance_pk; Type: CONSTRAINT; Schema: public; Owner: omar; Tablespace: 
--

ALTER TABLE ONLY reflectance
    ADD CONSTRAINT reflectance_pk PRIMARY KEY (id_landsat, latitude, longitude);


--
-- TOC entry 1909 (class 2606 OID 25063)
-- Name: date_landsat_cloud_fk; Type: FK CONSTRAINT; Schema: public; Owner: omar
--

ALTER TABLE ONLY discarded
    ADD CONSTRAINT date_landsat_cloud_fk FOREIGN KEY (id_landsat) REFERENCES date_landsat(id_landsat);


--
-- TOC entry 1908 (class 2606 OID 25068)
-- Name: date_landsat_radiance_fk; Type: FK CONSTRAINT; Schema: public; Owner: omar
--

ALTER TABLE ONLY radiance
    ADD CONSTRAINT date_landsat_radiance_fk FOREIGN KEY (id_landsat) REFERENCES date_landsat(id_landsat);


--
-- TOC entry 1907 (class 2606 OID 25073)
-- Name: date_landsat_value_pixel_fk; Type: FK CONSTRAINT; Schema: public; Owner: omar
--

ALTER TABLE ONLY reflectance
    ADD CONSTRAINT date_landsat_value_pixel_fk FOREIGN KEY (id_landsat) REFERENCES date_landsat(id_landsat);


--
-- TOC entry 2025 (class 0 OID 0)
-- Dependencies: 6
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2015-04-17 14:35:13 COT

--
-- PostgreSQL database dump complete
--

