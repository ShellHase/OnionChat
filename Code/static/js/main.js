function onSubAddName(name) {
    for (let i of document.getElementsByTagName("li")) {
        if (i.children[0].innerHTML == name.replace("_", " #")) {
            i.children[1].value = "—" + name;
        }
    }
}
