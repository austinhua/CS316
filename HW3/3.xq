<congress>
  <house> {
    for $p in /congress/people/person
    let $id := $p/@id
    where $p/role[@current=1 and @type="rep"]
      return
        <person name="{$p/@name}" > {
          for $c in /congress/committees/committee
          where $c/member/@id = $id
            return
              <committee name="{$c/@displayname}" role="{if ($c/member[@id = $id]/@role) then string($c/member[@id = $id]/@role) else ("Member")}" > {
                    for $sc in $c/subcommittee
                    where $sc/member/@id = $id
                    return
                      <subcommittee name="{$sc/@displayname}" role="{if ($sc/member[@id = $id]/@role) then string($sc/member[@id = $id]/@role) else ("Member") }" />
              } </committee>
        } </person>
  } </house>
  <senate> {
    for $p in /congress/people/person
    let $id := $p/@id
    where $p/role[@current=1 and @type="sen"]
      return
        <person name="{$p/@name}" > {
          for $c in /congress/committees/committee
          where $c/member/@id = $id
            return
              <committee name="{$c/@displayname}" role="{if ($c/member[@id = $id]/@role) then string($c/member[@id = $id]/@role) else ("Member")}" > {
                    for $sc in $c/subcommittee
                    where $sc/member/@id = $id
                    return
                      <subcommittee name="{$sc/@displayname}" role="{if ($sc/member[@id = $id]/@role) then string($sc/member[@id = $id]/@role) else ("Member") }" />
              } </committee>
        } </person>
  } </senate>
</congress>
