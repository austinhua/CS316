<result> {
  for $party in distinct-values(/congress/people/person/role[@current=1 and @type="rep"]/@party)
  let $count := count(/congress/people/person/role[@current=1 and @type="rep" and @party=$party])
  return
    <record count="{$count}" party="{$party}"/>
} </result>
