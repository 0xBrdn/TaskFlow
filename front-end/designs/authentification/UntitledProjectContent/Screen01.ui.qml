

/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/
import QtQuick
import QtQuick.Controls
import UntitledProject
import QtQuick.Studio.DesignEffects

Rectangle {
    id: main
    width: Constants.width
    height: Constants.height

    Image {
        id: background
        x: -20
        y: -112
        width: 1953
        height: 1290
        source: "../../../../../../Downloads/colorkit3.png"
        fillMode: Image.PreserveAspectFit
    }

    Rectangle {
        id: mireAuthentification
        x: 658
        y: 143
        width: 604
        height: 794
        color: "#b25c5c5c"
        radius: 13
        border.color: "#fc9840"
        border.width: 0

        Text {
            id: mainTitre
            x: 172
            y: 48
            width: 263
            height: 41
            color: "#ffffff"
            text: "S'identifier"
            font.pixelSize: 31
            horizontalAlignment: Text.AlignHCenter
            font.styleName: "Gras"
            font.family: "Tahoma"
        }

        Text {
            id: textMail
            x: 57
            y: 158
            width: 77
            height: 29
            color: "#ffffff"
            text: "E-mail"
            font.pixelSize: 21
            horizontalAlignment: Text.AlignHCenter
            font.styleName: "Gras"
            font.family: "Tahoma"

            Rectangle {
                id: containerMail
                x: 0
                y: 28
                width: 490
                height: 70
                color: "#5c5c5c"
                radius: 5

                TextInput {
                    id: inputMail
                    x: 15
                    y: 12
                    width: 460
                    height: 50
                    color: "#ffffff"
                    font.pixelSize: 17
                    horizontalAlignment: Text.AlignLeft
                    verticalAlignment: Text.AlignVCenter
                    selectionColor: "#b3c7c7c7"
                    font.bold: true
                    echoMode: TextInput.Normal
                    layer.enabled: true
                    maximumLength: 255
                    readOnly: false
                    property int newName: 0
                }
            }
        }

        Text {
            id: textPassword
            x: 57
            y: 281
            width: 125
            height: 31
            color: "#ffffff"
            text: "Mot de passe"
            font.pixelSize: 21
            horizontalAlignment: Text.AlignHCenter
            font.styleName: "Gras"
            font.family: "Tahoma"

            Rectangle {
                id: containerPassword
                x: 0
                y: 29
                width: 490
                height: 70
                color: "#5c5c5c"
                radius: 5
            }

            TextInput {
                id: inputPassword
                x: 15
                y: 39
                width: 460
                height: 50
                color: "#ffffff"
                font.pixelSize: 17
                horizontalAlignment: Text.AlignLeft
                verticalAlignment: Text.AlignVCenter
                selectionColor: "#b3c7c7c7"
                readOnly: false
                property int newName: 0
                maximumLength: 255
                layer.enabled: true
                font.bold: true
                echoMode: TextInput.Password
            }
        }

        Rectangle {
            id: rectangle8
            x: 194
            y: 671
            width: 211
            height: 74
            color: "#353637"
            radius: 5

            Button {
                id: button
                x: 11
                y: 3
                width: 190
                height: 68
                text: qsTr("Valider")
                flat: false
                z: 0
                scale: 1.106
                highlighted: false
                spacing: 5
                font.pointSize: 10
                font.bold: true
                font.family: "Tahoma"
                autoRepeat: true
                autoExclusive: true
                checkable: true
                checked: true
                display: AbstractButton.TextOnly
                font.weight: Font.Normal
            }
        }
    }

    DesignEffect {
        effects: [
            DesignDropShadow {}
        ]
    }
}
