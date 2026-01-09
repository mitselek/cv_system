CREATE MIGRATION m1kkpupp3eiuocjbkwykyjzmdng7vzjrdd4bilrw4gxzgwyrv4zbva
    ONTO initial
{
  CREATE TYPE default::Achievement {
      CREATE PROPERTY created: std::datetime {
          SET default := (std::datetime_current());
      };
      CREATE PROPERTY date: std::str;
      CREATE PROPERTY description: std::str;
      CREATE REQUIRED PROPERTY title: std::str;
  };
  CREATE TYPE default::Tag {
      CREATE REQUIRED PROPERTY category: std::str;
      CREATE REQUIRED PROPERTY name: std::str;
      CREATE CONSTRAINT std::exclusive ON ((.name, .category));
      CREATE PROPERTY created: std::datetime {
          SET default := (std::datetime_current());
      };
  };
  ALTER TYPE default::Achievement {
      CREATE MULTI LINK tags: default::Tag;
  };
  ALTER TYPE default::Tag {
      CREATE MULTI LINK achievements := (.<tags[IS default::Achievement]);
  };
  CREATE ABSTRACT TYPE default::ContextualEntity {
      CREATE LINK context: std::Object;
  };
  CREATE SCALAR TYPE default::CorrespondenceDirection EXTENDING enum<incoming, outgoing>;
  CREATE TYPE default::Correspondence EXTENDING default::ContextualEntity {
      CREATE REQUIRED PROPERTY body: std::str;
      CREATE REQUIRED PROPERTY date: std::datetime;
      CREATE REQUIRED PROPERTY direction: default::CorrespondenceDirection;
      CREATE PROPERTY email_file: std::str;
      CREATE PROPERTY from_address: std::str;
      CREATE PROPERTY subject: std::str;
      CREATE PROPERTY to_address: std::str;
  };
  CREATE SCALAR TYPE default::EventStatus EXTENDING enum<scheduled, completed, cancelled, rescheduled>;
  CREATE SCALAR TYPE default::EventType EXTENDING enum<interview, deadline, followup, meeting, other>;
  CREATE TYPE default::Event EXTENDING default::ContextualEntity {
      CREATE LINK rescheduled_from: default::Event;
      CREATE REQUIRED PROPERTY datetime: std::datetime;
      CREATE PROPERTY location: std::str;
      CREATE PROPERTY notes: std::str;
      CREATE PROPERTY rescheduled_reason: std::str;
      CREATE PROPERTY status: default::EventStatus {
          SET default := (default::EventStatus.scheduled);
      };
      CREATE REQUIRED PROPERTY type: default::EventType;
  };
  CREATE SCALAR TYPE default::Status EXTENDING enum<draft, ready, submitted, interview, offer, accepted, rejected, withdrawn>;
  CREATE TYPE default::Application {
      CREATE MULTI LINK correspondence := (.<context[IS default::Correspondence]);
      CREATE MULTI LINK events := (.<context[IS default::Event]);
      CREATE PROPERTY created_date: std::datetime {
          SET default := (std::datetime_current());
      };
      CREATE PROPERTY documents: std::json;
      CREATE PROPERTY fit_score: std::int16;
      CREATE PROPERTY notes: std::str;
      CREATE REQUIRED PROPERTY status: default::Status {
          SET default := (default::Status.draft);
      };
      CREATE PROPERTY submitted_date: std::datetime;
  };
  CREATE TYPE default::Posting {
      CREATE MULTI LINK correspondence := (.<context[IS default::Correspondence]);
      CREATE MULTI LINK events := (.<context[IS default::Event]);
      CREATE PROPERTY deadline: std::datetime;
      CREATE PROPERTY discovered_date: std::datetime {
          SET default := (std::datetime_current());
      };
      CREATE PROPERTY fit_score: std::int16;
      CREATE PROPERTY location: std::str;
      CREATE PROPERTY notes: std::str;
      CREATE PROPERTY posted_date: std::str;
      CREATE PROPERTY status: std::str;
      CREATE REQUIRED PROPERTY title: std::str;
      CREATE REQUIRED PROPERTY url: std::str {
          CREATE CONSTRAINT std::exclusive;
      };
  };
  ALTER TYPE default::Application {
      CREATE REQUIRED LINK posting: default::Posting;
  };
  ALTER TYPE default::Posting {
      CREATE MULTI LINK applications := (.<posting[IS default::Application]);
  };
  CREATE TYPE default::Company {
      CREATE PROPERTY created: std::datetime {
          SET default := (std::datetime_current());
      };
      CREATE REQUIRED PROPERTY name: std::str {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE PROPERTY notes: std::str;
  };
  ALTER TYPE default::Posting {
      CREATE REQUIRED LINK company: default::Company;
  };
  ALTER TYPE default::Company {
      CREATE MULTI LINK postings := (.<company[IS default::Posting]);
  };
  CREATE TYPE default::Experience {
      CREATE MULTI LINK tags: default::Tag;
      CREATE PROPERTY created: std::datetime {
          SET default := (std::datetime_current());
      };
      CREATE PROPERTY description_en: std::str;
      CREATE PROPERTY description_et: std::str;
      CREATE PROPERTY end_date: std::str;
      CREATE REQUIRED PROPERTY organization: std::str;
      CREATE REQUIRED PROPERTY start_date: std::str;
      CREATE REQUIRED PROPERTY title: std::str;
  };
  ALTER TYPE default::Tag {
      CREATE MULTI LINK experiences := (.<tags[IS default::Experience]);
  };
  CREATE TYPE default::Skill {
      CREATE MULTI LINK tags: default::Tag;
      CREATE PROPERTY created: std::datetime {
          SET default := (std::datetime_current());
      };
      CREATE PROPERTY description: std::str;
      CREATE PROPERTY evidence_refs: array<std::str>;
      CREATE PROPERTY level: std::int16;
      CREATE REQUIRED PROPERTY name: std::str {
          CREATE CONSTRAINT std::exclusive;
      };
  };
  ALTER TYPE default::Tag {
      CREATE MULTI LINK skills := (.<tags[IS default::Skill]);
  };
  CREATE SCALAR TYPE default::Language EXTENDING enum<en, et>;
};
