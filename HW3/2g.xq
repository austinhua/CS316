<result> {
  for $p in /congress/people/person
  where not(some $member in /congress/committees//member satisfies $member/@id=$p/@id)
  return
    <person>{string($p/@name)}</person>
} </result>
