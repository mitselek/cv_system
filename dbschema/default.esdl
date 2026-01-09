module default {
    # Shared types across domains
    scalar type Status extending enum<
        draft,
        ready,
        submitted,
        interview,
        offer,
        accepted,
        rejected,
        withdrawn
    >;

    scalar type EventType extending enum<
        interview,
        deadline,
        followup,
        meeting,
        other
    >;

    scalar type EventStatus extending enum<
        scheduled,
        completed,
        cancelled,
        rescheduled
    >;

    scalar type CorrespondenceDirection extending enum<
        incoming,
        outgoing
    >;

    scalar type Language extending enum<en, et>;

    # Applications Domain
    type Company {
        required property name -> str {
            constraint exclusive;
        }
        property notes -> str;
        property created -> datetime {
            default := datetime_current();
        }

        multi link postings := .<company[is Posting];
    }

    type Posting {
        required link company -> Company;
        required property url -> str {
            constraint exclusive;
        }
        required property title -> str;
        property location -> str;
        property posted_date -> str;
        property discovered_date -> datetime {
            default := datetime_current();
        }
        property deadline -> datetime;
        property status -> str;
        property fit_score -> int16;
        property notes -> str;

        multi link applications := .<posting[is Application];
        multi link correspondence := .<context[is Correspondence];
        multi link events := .<context[is Event];
    }

    type Application {
        required link posting -> Posting;
        required property status -> Status {
            default := Status.draft;
        }
        property created_date -> datetime {
            default := datetime_current();
        }
        property submitted_date -> datetime;
        property fit_score -> int16;
        property notes -> str;

        # Documents stored as JSON: {cv_et?: string, cv_en?: string, letter_et?: string, letter_en?: string}
        property documents -> json;

        multi link correspondence := .<context[is Correspondence];
        multi link events := .<context[is Event];
    }

    abstract type ContextualEntity {
        # Polymorphic reference - can point to Company, Posting, or Application
        link context -> Object;
    }

    type Correspondence extending ContextualEntity {
        required property direction -> CorrespondenceDirection;
        required property date -> datetime;
        property subject -> str;
        required property body -> str;
        property from_address -> str;
        property to_address -> str;
        property email_file -> str;
    }

    type Event extending ContextualEntity {
        required property type -> EventType;
        required property datetime -> datetime;
        property location -> str;
        property notes -> str;
        property status -> EventStatus {
            default := EventStatus.scheduled;
        }
        link rescheduled_from -> Event;
        property rescheduled_reason -> str;
    }

    # Knowledge Base Domain
    type Tag {
        required property name -> str;
        required property category -> str;
        property created -> datetime {
            default := datetime_current();
        }

        constraint exclusive on ((.name, .category));

        multi link experiences := .<tags[is Experience];
        multi link skills := .<tags[is Skill];
        multi link achievements := .<tags[is Achievement];
    }

    type Experience {
        required property title -> str;
        required property organization -> str;
        required property start_date -> str;
        property end_date -> str;
        property description_et -> str;
        property description_en -> str;
        property created -> datetime {
            default := datetime_current();
        }

        multi link tags -> Tag;
    }

    type Skill {
        required property name -> str {
            constraint exclusive;
        }
        property level -> int16;
        property description -> str;
        property evidence_refs -> array<str>;
        property created -> datetime {
            default := datetime_current();
        }

        multi link tags -> Tag;
    }

    type Achievement {
        required property title -> str;
        property date -> str;
        property description -> str;
        property created -> datetime {
            default := datetime_current();
        }

        multi link tags -> Tag;
    }
}
