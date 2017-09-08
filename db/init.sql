
CREATE TABLE individual(
    individual_id character varying(32) PRIMARY KEY,
    origin_id character varying(64) DEFAULT NULL,
    surname character varying (32) DEFAULT NULL,
    telephone character varying(11) NOT NULL,
    origin character varying(64) NOT NULL,
    created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- this will store standard associations (RS, EQ, HP, Ward Council, PEC) but also
-- could store members of a custom group (Lost Sheep Council)
CREATE TABLE association(
    association_id character varying(32) PRIMARY KEY,
    title character varying(32) NOT NULL
);

CREATE TABLE association_member(
     "association_member_id" character varying(32) PRIMARY KEY,
     "association_id" character varying(32) REFERENCES association,
     "individual_id" character varying(32) REFERENCES individual
);

CREATE TABLE message(
    message_id character varying(32) PRIMARY KEY,
    body character varying(1600) NOT NULL,
    sender character varying(32) REFERENCES individual NOT NULL,
    receiver character varying(32) REFERENCES individual NOT NULL,
    association_id character varying(32) REFERENCES association DEFAULT NULL,
    created TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    delivered BOOLEAN NOT NULL DEFAULT FALSE,
    viewed TIMESTAMP WITH TIME ZONE DEFAULT NULL,
    UNIQUE(message_id, sender, receiver)
);

CREATE TABLE twilio_message(
    twilio_message_id character varying(34) PRIMARY KEY, -- message_sid
    message_id character varying(32) REFERENCES message,
    "from" character varying(11) NOT NULL,
    "to" character varying(11) NOT NULL,
    status character varying(16) NOT NULL,
    error_code character varying(5) DEFAULT NULL,
    price character varying(6) DEFAULT NULL,
    price_unit character varying(3) DEFAULT NULL,
    updated TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

