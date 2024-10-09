

/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/
import QtQuick
import QtQuick.Controls
import Auth
import QtQuick.Studio.DesignEffects

Rectangle {
    id: main
    width: Constants.width
    height: Constants.height
    color: "#5c5c5c"
    radius: 0
    layer.smooth: false

    Image {
        id: image
        x: 0
        y: 0
        width: 1920
        height: 1080
        source: "../../Downloads/colorkit3.png"
        autoTransform: false
        asynchronous: false
        fillMode: Image.PreserveAspectFit
    }
    Rectangle {
        id: mireAuth
        x: 607
        y: 96
        width: 707
        height: 889
        color: "#b25c5c5c"
        radius: 25
        border.color: "#e74c3c"
        border.width: 0

        TextField {
            id: login
            x: 194
            y: 106
            width: 319
            height: 89
            color: "#fc9840"
            horizontalAlignment: Text.AlignHCenter
            selectedTextColor: "#fe5f75"
            placeholderTextColor: "#b3fe5f75"
            selectionColor: "#fc9840"
            font.pointSize: 15
            placeholderText: qsTr("Entez votre identifiant")
        }
    }
}

/*##^##
Designer {
    D{i:0}D{i:1;locked:true}
}
##^##*/

