# Before and after 6X6

6X6 should be understandable before it is installable.

## Before

A normal AI answer may begin with context, caveats, background, and several paragraphs before reaching the useful part.

> There are several ways to approach this. The right answer depends on your environment, priorities, and constraints. In general, I would first review the failing tests, determine whether the issue is isolated, inspect the authentication changes, and then decide whether the pull request is safe to merge...

## After 6X6

```text
Do not merge yet.
Two tests are still failing.
Fix the authentication regression first.
Run the full test suite.
Merge when everything passes.
```

Need the reasoning? Ask:

```text
Expand line 3.
```

6X6 does not remove the details. It moves them behind the first useful answer.
