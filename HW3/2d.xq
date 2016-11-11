<result> {
  for $p in /congress/people/person
  let $r := $p/role[@current=1]
  where $r/@state="NC" and $r/@type="rep"
  order by xs:integer($r/@district)
  return
    <representative name="{$p/@name}" district="{$r/@district}" party="{$r/@party}" />
} </result>
