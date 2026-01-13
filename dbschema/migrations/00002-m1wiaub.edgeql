CREATE MIGRATION m1wiaubswja4sw754vuz5uxiowb73r7fqts5xzhcvxwln3pgiqhlxa
    ONTO m1ql2jhtfy35hy2hn4daxd77xix5bi7yn2lq7llfblkuwq4ct7ossq
{
  CREATE FUNCTION default::get_text(t: default::Translation, lang: std::str) ->  std::str USING ((<std::str>(t)[lang] ?? (<std::str>(t)['et'] ?? (<std::str>(t)['en'] ?? ''))));
  ALTER TYPE default::Experience {
      CREATE PROPERTY company_en := (default::get_text(.company, 'en'));
      CREATE PROPERTY company_et := (default::get_text(.company, 'et'));
      CREATE PROPERTY title_en := (default::get_text(.title, 'en'));
      CREATE PROPERTY title_et := (default::get_text(.title, 'et'));
  };
  ALTER TYPE default::Hobby {
      CREATE PROPERTY display_name := (default::get_text(.name, 'en'));
      CREATE PROPERTY name_en := (default::get_text(.name, 'en'));
      CREATE PROPERTY name_et := (default::get_text(.name, 'et'));
  };
  ALTER TYPE default::KnowledgeBaseLanguage {
      CREATE PROPERTY display_name := (default::get_text(.name, 'en'));
      CREATE PROPERTY name_en := (default::get_text(.name, 'en'));
      CREATE PROPERTY name_et := (default::get_text(.name, 'et'));
  };
  ALTER TYPE default::Project {
      CREATE PROPERTY display_name := (default::get_text(.name, 'en'));
      CREATE PROPERTY name_en := (default::get_text(.name, 'en'));
      CREATE PROPERTY name_et := (default::get_text(.name, 'et'));
  };
  ALTER TYPE default::Skill {
      CREATE PROPERTY display_name := (default::get_text(.name, 'en'));
      CREATE PROPERTY name_en := (default::get_text(.name, 'en'));
      CREATE PROPERTY name_et := (default::get_text(.name, 'et'));
  };
  ALTER TYPE default::Certification {
      CREATE PROPERTY issuer_en := (default::get_text(.issuer, 'en'));
      CREATE PROPERTY issuer_et := (default::get_text(.issuer, 'et'));
      CREATE PROPERTY title_en := (default::get_text(.title, 'en'));
      CREATE PROPERTY title_et := (default::get_text(.title, 'et'));
  };
  ALTER TYPE default::Achievement {
      CREATE PROPERTY title_en := (default::get_text(.title, 'en'));
      CREATE PROPERTY title_et := (default::get_text(.title, 'et'));
  };
};
