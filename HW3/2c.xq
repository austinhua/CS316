<result> {
  for $p in /congress/people/person
  where $p/role[@type = 'sen' and @current = 1] and $p[@gender = 'F'] and xs:date($p/@birthday) < xs:date('1940-01-01')
  return
    <senator name="{$p/@name}"/>
} </result>
