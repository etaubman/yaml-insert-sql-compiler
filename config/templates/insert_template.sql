-- {{ metadata.comment }}
INSERT INTO {{ mappings.table_mappings[definition.table].table_name }} ({% for field in definition.fields %}{{ field }}{% if not loop.last %},{% endif %}{% endfor %}) VALUES ({% for value in definition["values"] %}{% if value is is_string %}'{{ value }}'{% elif value is is_raw %}{{ value.raw }}{% else %}{{ value }}{% endif %}{% if not loop.last %},{% endif %}{% endfor %});