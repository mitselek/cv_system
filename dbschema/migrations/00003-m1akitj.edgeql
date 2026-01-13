CREATE MIGRATION m1akitjquawfhxkslovnjfaizc7miudetyorwaxphmcax2ssuqr2qa
    ONTO m1wiaubswja4sw754vuz5uxiowb73r7fqts5xzhcvxwln3pgiqhlxa
{
  ALTER FUNCTION default::get_text(t: default::Translation, lang: std::str) USING ((<std::str>std::json_get(t, lang) ?? (<std::str>std::json_get(t, 'et') ?? (<std::str>std::json_get(t, 'en') ?? ''))));
};
