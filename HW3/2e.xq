<result> {
  for $p in /congress/people/person
  let $cr := $p/role[@current=1]
  where $cr/@type="sen" and (some $r in $p/role satisfies $r/@type="rep")
  return
    <member>{string($p/@name)}</member>
} </result>
