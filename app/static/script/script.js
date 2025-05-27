function toggleSettings() {
    settingsBox = document.getElementById("settings");
    if (settingsBox.style.display == "block") {
        settingsBox.style.display = "none";
    }
    else {
        settingsBox.style.display = "block";
    }
}
function toggleMobileSettings() {
    settingsBox = document.getElementById("mobile-settings");
    if (settingsBox.style.display == "block") {
        settingsBox.style.display = "none";
    }
    else {
        settingsBox.style.display = "block";
    }
}
function toggleWideSettings() {
    settingsBox = document.getElementById("wide-settings");
    if (settingsBox.style.display == "block") {
        settingsBox.style.display = "none";
    }
    else {
        settingsBox.style.display = "block";
    }
}
function openNav() {
    document.getElementById("sidenav").style.width = "150px";
}

function closeNav() {
    document.getElementById("sidenav").style.width = "0";
}

function setLightTheme(page) {
    var root = document.querySelector(':root');
    root.style.setProperty("--bg-primary", "#f5f5f6");
    root.style.setProperty("--bg-secondry", "#c2c2c3");

    root.style.setProperty("--fg-primary", "#1c1c1c");
    root.style.setProperty("--fg-secondry", "#434343");
    root.style.setProperty("--secondry", "#000000");
    if (page == "landing") {
        document.querySelector(".logo h1").style.color = "var(--primary)";
    }
    else if (page == "results-mobile") {
        document.querySelector(".res header.header-mobile").style.background = "var(--bg-secondry)";
        document.querySelector(".res header.header-mobile .logo").style.color = "var(--primary)";
    }
    else if (page == "results-wide") {
        document.querySelector(".res header.header-wide").style.background = "var(--bg-secondry)";
        document.querySelector(".res header.header-wide .logo").style.color = "var(--primary)";
    }
    localStorage.setItem("theme", "light");
}
function setDarkTheme(page) {
    var root = document.querySelector(':root');
    root.style.setProperty("--bg-primary", "#1c1c1c");
    root.style.setProperty("--bg-secondry", "#434343");

    root.style.setProperty("--fg-primary", "#f5f5f6");
    root.style.setProperty("--fg-secondry", "#c2c2c3");
    root.style.setProperty("--secondry", "#ffffff");
    if (page == "landing") {
        document.querySelector(".logo h1").style.color = "var(--fg-primary)";
    }
    else if (page == "results-mobile") {
        document.querySelector(".res header.header-mobile .logo").style.color = "var(--fg-primary)";
    }
    else if (page == "results-wide") {
        document.querySelector(".res header.header-wide .logo").style.color = "var(--fg-primary)";
    }
    localStorage.setItem("theme", "dark");
}