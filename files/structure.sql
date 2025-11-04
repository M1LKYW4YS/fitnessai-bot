--
-- PostgreSQL database dump
--

\restrict KJdHrWUnOt3AfLw5VHoIzuS7diofH17qH28gKBA1uze0BACyEj92ZHcifVT0qwS

-- Dumped from database version 17.6
-- Dumped by pg_dump version 17.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: activity_level; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.activity_level AS ENUM (
    'low',
    'medium',
    'high'
);


ALTER TYPE public.activity_level OWNER TO postgres;

--
-- Name: experience_level; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.experience_level AS ENUM (
    'beginner',
    'intermediate',
    'advanced'
);


ALTER TYPE public.experience_level OWNER TO postgres;

--
-- Name: gender; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.gender AS ENUM (
    'male',
    'female',
    'other'
);


ALTER TYPE public.gender OWNER TO postgres;

--
-- Name: meal_type; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.meal_type AS ENUM (
    'breakfast',
    'lunch',
    'dinner',
    'snack'
);


ALTER TYPE public.meal_type OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: ai_chat_logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ai_chat_logs (
    id integer NOT NULL,
    user_id integer,
    "timestamp" timestamp without time zone NOT NULL,
    user_input text NOT NULL,
    ai_response text NOT NULL
);


ALTER TABLE public.ai_chat_logs OWNER TO postgres;

--
-- Name: ai_chat_logs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ai_chat_logs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ai_chat_logs_id_seq OWNER TO postgres;

--
-- Name: ai_chat_logs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ai_chat_logs_id_seq OWNED BY public.ai_chat_logs.id;


--
-- Name: exercise_logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.exercise_logs (
    id integer NOT NULL,
    user_id integer,
    date date NOT NULL,
    exercise text NOT NULL,
    sets integer NOT NULL,
    reps integer NOT NULL,
    weight_used numeric
);


ALTER TABLE public.exercise_logs OWNER TO postgres;

--
-- Name: exercise_logs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.exercise_logs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.exercise_logs_id_seq OWNER TO postgres;

--
-- Name: exercise_logs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.exercise_logs_id_seq OWNED BY public.exercise_logs.id;


--
-- Name: fitness_locations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fitness_locations (
    id integer NOT NULL,
    name text NOT NULL,
    address text NOT NULL,
    latitude numeric NOT NULL,
    longitude numeric NOT NULL,
    category text NOT NULL,
    description text
);


ALTER TABLE public.fitness_locations OWNER TO postgres;

--
-- Name: fitness_locations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.fitness_locations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.fitness_locations_id_seq OWNER TO postgres;

--
-- Name: fitness_locations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.fitness_locations_id_seq OWNED BY public.fitness_locations.id;


--
-- Name: foods; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.foods (
    id integer NOT NULL,
    name text NOT NULL,
    calories integer NOT NULL,
    protein numeric NOT NULL,
    fat numeric NOT NULL,
    carbs numeric NOT NULL,
    is_custom boolean NOT NULL,
    user_id integer
);


ALTER TABLE public.foods OWNER TO postgres;

--
-- Name: foods_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.foods_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.foods_id_seq OWNER TO postgres;

--
-- Name: foods_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.foods_id_seq OWNED BY public.foods.id;


--
-- Name: meal_items; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.meal_items (
    id integer NOT NULL,
    meal_id integer,
    food_id integer,
    grams numeric NOT NULL
);


ALTER TABLE public.meal_items OWNER TO postgres;

--
-- Name: meal_items_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.meal_items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.meal_items_id_seq OWNER TO postgres;

--
-- Name: meal_items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.meal_items_id_seq OWNED BY public.meal_items.id;


--
-- Name: meals; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.meals (
    id integer NOT NULL,
    user_id integer,
    date date NOT NULL,
    meal_type public.meal_type NOT NULL
);


ALTER TABLE public.meals OWNER TO postgres;

--
-- Name: meals_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.meals_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.meals_id_seq OWNER TO postgres;

--
-- Name: meals_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.meals_id_seq OWNED BY public.meals.id;


--
-- Name: measurements; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.measurements (
    id integer NOT NULL,
    user_id integer,
    date date NOT NULL,
    weight numeric NOT NULL,
    waist_cm numeric,
    chest_cm numeric,
    hip_cm numeric,
    pulse integer
);


ALTER TABLE public.measurements OWNER TO postgres;

--
-- Name: measurements_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.measurements_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.measurements_id_seq OWNER TO postgres;

--
-- Name: measurements_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.measurements_id_seq OWNED BY public.measurements.id;


--
-- Name: program_templates; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.program_templates (
    id integer NOT NULL,
    title text NOT NULL,
    category text NOT NULL,
    description text,
    duration_weeks integer NOT NULL
);


ALTER TABLE public.program_templates OWNER TO postgres;

--
-- Name: program_templates_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.program_templates_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.program_templates_id_seq OWNER TO postgres;

--
-- Name: program_templates_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.program_templates_id_seq OWNED BY public.program_templates.id;


--
-- Name: user_programs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_programs (
    id integer NOT NULL,
    user_id integer,
    template_id integer,
    created_at timestamp without time zone NOT NULL,
    is_active boolean NOT NULL
);


ALTER TABLE public.user_programs OWNER TO postgres;

--
-- Name: user_programs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_programs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_programs_id_seq OWNER TO postgres;

--
-- Name: user_programs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_programs_id_seq OWNED BY public.user_programs.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id bigint NOT NULL,
    name text NOT NULL,
    email text,
    password_hash text,
    age integer,
    sex public.gender,
    height_cm integer,
    weight_kg numeric(5,2),
    activity_level public.activity_level,
    fitness_goal text,
    disability_status boolean,
    experience_level public.experience_level,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: ai_chat_logs id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ai_chat_logs ALTER COLUMN id SET DEFAULT nextval('public.ai_chat_logs_id_seq'::regclass);


--
-- Name: exercise_logs id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exercise_logs ALTER COLUMN id SET DEFAULT nextval('public.exercise_logs_id_seq'::regclass);


--
-- Name: fitness_locations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fitness_locations ALTER COLUMN id SET DEFAULT nextval('public.fitness_locations_id_seq'::regclass);


--
-- Name: foods id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.foods ALTER COLUMN id SET DEFAULT nextval('public.foods_id_seq'::regclass);


--
-- Name: meal_items id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.meal_items ALTER COLUMN id SET DEFAULT nextval('public.meal_items_id_seq'::regclass);


--
-- Name: meals id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.meals ALTER COLUMN id SET DEFAULT nextval('public.meals_id_seq'::regclass);


--
-- Name: measurements id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.measurements ALTER COLUMN id SET DEFAULT nextval('public.measurements_id_seq'::regclass);


--
-- Name: program_templates id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.program_templates ALTER COLUMN id SET DEFAULT nextval('public.program_templates_id_seq'::regclass);


--
-- Name: user_programs id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_programs ALTER COLUMN id SET DEFAULT nextval('public.user_programs_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: ai_chat_logs ai_chat_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ai_chat_logs
    ADD CONSTRAINT ai_chat_logs_pkey PRIMARY KEY (id);


--
-- Name: exercise_logs exercise_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exercise_logs
    ADD CONSTRAINT exercise_logs_pkey PRIMARY KEY (id);


--
-- Name: fitness_locations fitness_locations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fitness_locations
    ADD CONSTRAINT fitness_locations_pkey PRIMARY KEY (id);


--
-- Name: foods foods_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.foods
    ADD CONSTRAINT foods_pkey PRIMARY KEY (id);


--
-- Name: meal_items meal_items_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.meal_items
    ADD CONSTRAINT meal_items_pkey PRIMARY KEY (id);


--
-- Name: meals meals_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.meals
    ADD CONSTRAINT meals_pkey PRIMARY KEY (id);


--
-- Name: measurements measurements_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.measurements
    ADD CONSTRAINT measurements_pkey PRIMARY KEY (id);


--
-- Name: program_templates program_templates_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.program_templates
    ADD CONSTRAINT program_templates_pkey PRIMARY KEY (id);


--
-- Name: user_programs user_programs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_programs
    ADD CONSTRAINT user_programs_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ai_chat_logs ai_chat_logs_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ai_chat_logs
    ADD CONSTRAINT ai_chat_logs_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: exercise_logs exercise_logs_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exercise_logs
    ADD CONSTRAINT exercise_logs_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: foods foods_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.foods
    ADD CONSTRAINT foods_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: meal_items meal_items_food_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.meal_items
    ADD CONSTRAINT meal_items_food_id_fkey FOREIGN KEY (food_id) REFERENCES public.foods(id);


--
-- Name: meal_items meal_items_meal_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.meal_items
    ADD CONSTRAINT meal_items_meal_id_fkey FOREIGN KEY (meal_id) REFERENCES public.meals(id);


--
-- Name: meals meals_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.meals
    ADD CONSTRAINT meals_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: measurements measurements_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.measurements
    ADD CONSTRAINT measurements_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: user_programs user_programs_template_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_programs
    ADD CONSTRAINT user_programs_template_id_fkey FOREIGN KEY (template_id) REFERENCES public.program_templates(id);


--
-- Name: user_programs user_programs_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_programs
    ADD CONSTRAINT user_programs_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

\unrestrict KJdHrWUnOt3AfLw5VHoIzuS7diofH17qH28gKBA1uze0BACyEj92ZHcifVT0qwS

