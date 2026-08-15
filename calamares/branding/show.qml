/* Borealis Linux — installer slideshow (auto-advancing, quiet). */
import QtQuick 2.0;

Presentation {
    id: presentation
    timerFunction: function() { }   // advance manually via Timer below

    Timer {
        interval: 6000
        running: true
        repeat: true
        onTriggered: presentation.goToNextSlide()
    }

    Slide {
        centeredText: qsTr("Welcome to Borealis Linux\n\nA fast, calm desktop for people\nleaving Windows and macOS behind.")
    }

    Slide {
        centeredText: qsTr("Your apps, one store\n\nAPT · Flatpak · Snap · AppImage —\none search box, one click.\nWindows programs run out of the box.")
    }

    Slide {
        centeredText: qsTr("Built to last\n\nRuns great on a 2008 laptop,\nfaster still on a 2026 desktop.\nTake your time — nothing is being sent anywhere.")
    }
}
