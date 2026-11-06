
# Check whether an element is a variable
def is_variable(x):
    return isinstance(x, str) and x.startswith("?")


# Apply substitutions
def substitute(x, theta):
    if is_variable(x) and x in theta:
        return substitute(theta[x], theta)

    if isinstance(x, tuple):
        return tuple(substitute(i, theta) for i in x)

    return x


# Occurs check
def occurs(var, x, theta):
    x = substitute(x, theta)

    if var == x:
        return True

    if isinstance(x, tuple):
        return any(occurs(var, i, theta) for i in x)

    return False


# Unification algorithm
def unify(x, y, theta=None):
    if theta is None:
        theta = {}

    x = substitute(x, theta)
    y = substitute(y, theta)

    if x == y:
        return theta

    if is_variable(x):
        if occurs(x, y, theta):
            return None
        theta[x] = y
        return theta

    if is_variable(y):
        if occurs(y, x, theta):
            return None
        theta[y] = x
        return theta

    if isinstance(x, tuple) and isinstance(y, tuple):

        if x[0] != y[0] or len(x) != len(y):
            return None

        for a, b in zip(x[1:], y[1:]):
            theta = unify(a, b, theta)

            if theta is None:
                return None

        return theta

    return None


# Give rule variables new names
def standardize(rule, count):
    mapping = {}

    def rename(x):
        if is_variable(x):
            if x not in mapping:
                mapping[x] = x + "_" + str(count)
            return mapping[x]

        if isinstance(x, tuple):
            return tuple(rename(i) for i in x)

        return x

    premises, conclusion = rule

    return ([rename(p) for p in premises],
            rename(conclusion))


# Match all premises of a rule with KB facts
def match_premises(premises, kb, theta):

    if not premises:
        return [theta]

    first = substitute(premises[0], theta)
    remaining = premises[1:]

    results = []

    for fact in kb:
        new_theta = unify(first, fact, theta.copy())

        if new_theta is not None:
            results.extend(
                match_premises(remaining, kb, new_theta)
            )

    return results


# Forward Chaining Algorithm
def forward_chaining(KB, query):

    count = 0

    while True:

        new = []

        # Check each rule in KB
        for rule in KB["rules"]:

            count += 1

            # Standardize variables
            premises, conclusion = standardize(rule, count)

            # Find substitutions satisfying all premises
            substitutions = match_premises(
                premises, KB["facts"], {}
            )

            for theta in substitutions:

                # Apply substitution to conclusion
                q = substitute(conclusion, theta)

                # Check whether query matches the conclusion
                result = unify(query, q)

                if result is not None:
                    return result

                # Add only new facts
                if q not in KB["facts"] and q not in new:
                    new.append(q)

        # If no new facts are generated
        if not new:
            return False

        # Add new facts to Knowledge Base
        KB["facts"].extend(new)


# Main Program

KB = {

    "facts": [
        ("Parent", "John", "Mary"),
        ("Parent", "Mary", "Sam"),
        ("Parent", "Sam", "Tom")
    ],

    "rules": [

        (
            [
                ("Parent", "?x", "?y"),
                ("Parent", "?y", "?z")
            ],
            ("Grandparent", "?x", "?z")
        )
    ]
}

# Query
query = ("Grandparent", "John", "?who")

result = forward_chaining(KB, query)

if result:
    print("Query is TRUE")
    print("Substitution:", result)
else:
    print("Query is FALSE")
