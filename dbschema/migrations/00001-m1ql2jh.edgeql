CREATE MIGRATION m1ql2jhtfy35hy2hn4daxd77xix5bi7yn2lq7llfblkuwq4ct7ossq
    ONTO initial
{
  CREATE SCALAR TYPE default::Translation EXTENDING std::json {
      CREATE CONSTRAINT std::expression ON (((std::len((<std::str>std::json_get(__subject__, 'et') ?? '')) > 0) OR (std::len((<std::str>std::json_get(__subject__, 'en') ?? '')) > 0))) {
          SET errmessage := 'At least one language (et or en) must be provided';
      };
  };
  CREATE SCALAR TYPE default::IsoDate EXTENDING std::str {
      CREATE CONSTRAINT std::regexp(r'^\d{4}(-\d{2}(-\d{2})?)?$') {
          SET errmessage := 'Date must be in YYYY, YYYY-MM, or YYYY-MM-DD format';
      };
  };
  CREATE SCALAR TYPE default::VerificationStatus EXTENDING enum<verified, draft, outdated>;
  CREATE TYPE default::Education {
      CREATE REQUIRED PROPERTY fields: array<default::Translation>;
      CREATE REQUIRED PROPERTY institutions: array<default::Translation>;
      CREATE PROPERTY article: default::Translation;
      CREATE PROPERTY created: std::datetime {
          SET default := (std::datetime_current());
      };
      CREATE REQUIRED PROPERTY dates: tuple<`start`: default::IsoDate, `end`: default::IsoDate>;
      CREATE PROPERTY degree: default::Translation;
      CREATE REQUIRED PROPERTY external_id: std::str {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE REQUIRED PROPERTY last_verified: default::IsoDate;
      CREATE REQUIRED PROPERTY verification_status: default::VerificationStatus {
          SET default := (default::VerificationStatus.draft);
      };
  };
  CREATE TYPE default::Achievement {
      CREATE PROPERTY article: default::Translation;
      CREATE PROPERTY created: std::datetime {
          SET default := (std::datetime_current());
      };
      CREATE REQUIRED PROPERTY date: default::IsoDate;
      CREATE REQUIRED PROPERTY external_id: std::str {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE REQUIRED PROPERTY last_verified: default::IsoDate;
      CREATE REQUIRED PROPERTY title: default::Translation;
      CREATE REQUIRED PROPERTY verification_status: default::VerificationStatus {
          SET default := (default::VerificationStatus.draft);
      };
  };
  CREATE SCALAR TYPE default::HttpUrl EXTENDING std::str {
      CREATE CONSTRAINT std::regexp(r'^https?://[^\s]+$') {
          SET errmessage := 'Invalid HTTP/HTTPS URL format';
      };
  };
  CREATE TYPE default::Experience {
      CREATE PROPERTY article: default::Translation;
      CREATE REQUIRED PROPERTY company: default::Translation;
      CREATE PROPERTY created: std::datetime {
          SET default := (std::datetime_current());
      };
      CREATE REQUIRED PROPERTY dates: tuple<`start`: default::IsoDate, `end`: default::IsoDate>;
      CREATE REQUIRED PROPERTY external_id: std::str {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE REQUIRED PROPERTY last_verified: default::IsoDate;
      CREATE REQUIRED PROPERTY title: default::Translation;
      CREATE PROPERTY url: default::HttpUrl;
      CREATE REQUIRED PROPERTY verification_status: default::VerificationStatus {
          SET default := (default::VerificationStatus.draft);
      };
  };
  ALTER TYPE default::Achievement {
      CREATE LINK parent_experience: default::Experience;
  };
  ALTER TYPE default::Experience {
      CREATE MULTI LINK achievements := (.<parent_experience[IS default::Achievement]);
  };
  CREATE TYPE default::Tag {
      CREATE REQUIRED PROPERTY category: std::str;
      CREATE REQUIRED PROPERTY name: std::str;
      CREATE CONSTRAINT std::exclusive ON ((.name, .category));
      CREATE PROPERTY created: std::datetime {
          SET default := (std::datetime_current());
      };
      CREATE REQUIRED PROPERTY last_verified: default::IsoDate;
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
  CREATE TYPE default::Certification {
      CREATE MULTI LINK tags: default::Tag;
      CREATE PROPERTY article: default::Translation;
      CREATE PROPERTY created: std::datetime {
          SET default := (std::datetime_current());
      };
      CREATE PROPERTY credential_id: std::str;
      CREATE PROPERTY credential_url: default::HttpUrl;
      CREATE REQUIRED PROPERTY date: default::IsoDate;
      CREATE PROPERTY expiry_date: default::IsoDate;
      CREATE REQUIRED PROPERTY external_id: std::str {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE REQUIRED PROPERTY issuer: default::Translation;
      CREATE REQUIRED PROPERTY last_verified: default::IsoDate;
      CREATE REQUIRED PROPERTY title: default::Translation;
      CREATE REQUIRED PROPERTY verification_status: default::VerificationStatus {
          SET default := (default::VerificationStatus.draft);
      };
  };
  ALTER TYPE default::Tag {
      CREATE MULTI LINK certifications := (.<tags[IS default::Certification]);
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
  ALTER TYPE default::Education {
      CREATE MULTI LINK tags: default::Tag;
  };
  ALTER TYPE default::Tag {
      CREATE MULTI LINK education_entries := (.<tags[IS default::Education]);
  };
  CREATE SCALAR TYPE default::SkillCategory EXTENDING enum<programming_language, backend_development, frontend_development, database, devops, cloud_platform, framework, tool, methodology, soft_skill, domain_knowledge, testing, security, other>;
  CREATE TYPE default::Skill {
      CREATE MULTI LINK tags: default::Tag;
      CREATE PROPERTY article: default::Translation;
      CREATE REQUIRED PROPERTY category: default::SkillCategory;
      CREATE PROPERTY created: std::datetime {
          SET default := (std::datetime_current());
      };
      CREATE REQUIRED PROPERTY external_id: std::str {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE REQUIRED PROPERTY last_verified: default::IsoDate;
      CREATE REQUIRED PROPERTY level: std::int16 {
          CREATE CONSTRAINT std::max_value(10);
          CREATE CONSTRAINT std::min_value(1);
      };
      CREATE PROPERTY level_display: std::str;
      CREATE REQUIRED PROPERTY name: default::Translation;
      CREATE REQUIRED PROPERTY verification_status: default::VerificationStatus {
          SET default := (default::VerificationStatus.draft);
      };
  };
  ALTER TYPE default::Experience {
      CREATE MULTI LINK skills_demonstrated: default::Skill;
      CREATE MULTI LINK tags: default::Tag;
  };
  ALTER TYPE default::Skill {
      CREATE MULTI LINK demonstrated_in := (.<skills_demonstrated[IS default::Experience]);
  };
  ALTER TYPE default::Tag {
      CREATE MULTI LINK experiences := (.<tags[IS default::Experience]);
  };
  CREATE SCALAR TYPE default::LanguageProficiency EXTENDING std::json;
  CREATE TYPE default::KnowledgeBaseLanguage {
      CREATE MULTI LINK evidence: default::Experience;
      CREATE MULTI LINK tags: default::Tag;
      CREATE PROPERTY article: default::Translation;
      CREATE PROPERTY created: std::datetime {
          SET default := (std::datetime_current());
      };
      CREATE REQUIRED PROPERTY external_id: std::str {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE REQUIRED PROPERTY last_verified: default::IsoDate;
      CREATE REQUIRED PROPERTY name: default::Translation;
      CREATE REQUIRED PROPERTY proficiency: default::LanguageProficiency;
      CREATE REQUIRED PROPERTY verification_status: default::VerificationStatus {
          SET default := (default::VerificationStatus.draft);
      };
  };
  CREATE TYPE default::Hobby {
      CREATE MULTI LINK tags: default::Tag;
      CREATE PROPERTY article: default::Translation;
      CREATE PROPERTY created: std::datetime {
          SET default := (std::datetime_current());
      };
      CREATE REQUIRED PROPERTY external_id: std::str {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE REQUIRED PROPERTY last_verified: default::IsoDate;
      CREATE REQUIRED PROPERTY name: default::Translation;
      CREATE PROPERTY tools: array<std::str>;
      CREATE REQUIRED PROPERTY verification_status: default::VerificationStatus {
          SET default := (default::VerificationStatus.draft);
      };
  };
  ALTER TYPE default::Tag {
      CREATE MULTI LINK hobbies := (.<tags[IS default::Hobby]);
      CREATE MULTI LINK languages := (.<tags[IS default::KnowledgeBaseLanguage]);
  };
  CREATE SCALAR TYPE default::ProjectStatus EXTENDING enum<active, completed, archived>;
  CREATE TYPE default::Project {
      CREATE MULTI LINK skills_demonstrated: default::Skill;
      CREATE MULTI LINK tags: default::Tag;
      CREATE PROPERTY article: default::Translation;
      CREATE PROPERTY created: std::datetime {
          SET default := (std::datetime_current());
      };
      CREATE PROPERTY dates: tuple<`start`: default::IsoDate, `end`: default::IsoDate>;
      CREATE REQUIRED PROPERTY external_id: std::str {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE REQUIRED PROPERTY last_verified: default::IsoDate;
      CREATE REQUIRED PROPERTY name: default::Translation;
      CREATE PROPERTY repository: default::HttpUrl;
      CREATE REQUIRED PROPERTY status: default::ProjectStatus {
          SET default := (default::ProjectStatus.active);
      };
      CREATE PROPERTY technologies: array<std::str>;
      CREATE PROPERTY url: default::HttpUrl;
      CREATE REQUIRED PROPERTY verification_status: default::VerificationStatus {
          SET default := (default::VerificationStatus.draft);
      };
  };
  ALTER TYPE default::Skill {
      CREATE MULTI LINK used_in_projects := (.<skills_demonstrated[IS default::Project]);
  };
  ALTER TYPE default::Tag {
      CREATE MULTI LINK projects := (.<tags[IS default::Project]);
      CREATE MULTI LINK skills := (.<tags[IS default::Skill]);
  };
  CREATE SCALAR TYPE default::Language EXTENDING enum<en, et>;
};
