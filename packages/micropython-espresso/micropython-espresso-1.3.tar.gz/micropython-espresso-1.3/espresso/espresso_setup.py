BOOT = '/boot.py'

activated = "from espresso import espresso"
deactivated = "#from espresso import espresso"

# Read current boot status
with open(BOOT, 'r') as file:
    content = file.read()


# ----------------------------------------------------------------------
def espresso_enable():
    """"""
    global content

    content = content.replace(deactivated, '')
    content = content.replace(activated, '')

    with open(BOOT, 'w') as file:
        file.write('{}\n{}'.format(content, activated))


# ----------------------------------------------------------------------
def espresso_disable():
    """"""
    global content

    content = content.replace(deactivated, '')
    content = content.replace(activated, '')

    with open(BOOT, 'w') as file:
        file.write('{}\n{}'.format(content, deactivated))

