from PyQt5 import QtCore, QtGui, QtWidgets
from backend.db_api import DB_API


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # ... (keep all existing setup code until frameMire) ...

        # Modify the frameMire setup to enable animations
        self.frameMire = QtWidgets.QFrame(self.centralwidget)
        self.frameMire.setMinimumSize(QtCore.QSize(350, 500))
        self.frameMire.setMaximumSize(QtCore.QSize(350, 500))
        self.frameMire.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameMire.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameMire.setObjectName("frameMire")

        # Add opacity effect for fade animation
        self.opacity_effect = QtWidgets.QGraphicsOpacityEffect(self.frameMire)
        self.opacity_effect.setOpacity(1.0)
        self.frameMire.setGraphicsEffect(self.opacity_effect)

        # Create animations
        self.fade_out_animation = QtCore.QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_out_animation.setDuration(300)  # 300ms duration
        self.fade_out_animation.setStartValue(1.0)
        self.fade_out_animation.setEndValue(0.0)
        self.fade_out_animation.setEasingCurve(QtCore.QEasingCurve.InOutQuad)

        self.fade_in_animation = QtCore.QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_in_animation.setDuration(300)  # 300ms duration
        self.fade_in_animation.setStartValue(0.0)
        self.fade_in_animation.setEndValue(1.0)
        self.fade_in_animation.setEasingCurve(QtCore.QEasingCurve.InOutQuad)

        # Create slide animation
        self.slide_animation = QtCore.QPropertyAnimation(self.frameMire, b"geometry")
        self.slide_animation.setDuration(300)  # 300ms duration
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve.InOutQuad)

        # Connect animation finished signals
        self.fade_out_animation.finished.connect(self.on_fade_out_finished)
        self.fade_in_animation.finished.connect(self.on_fade_in_finished)

        # ... (keep rest of the existing setup code) ...

    def show_signup_form(self):
        """Start the animation sequence to switch forms"""
        if not self.fade_out_animation.state() == QtCore.QAbstractAnimation.Running:
            # Store the target state
            self.target_is_login_form = not self.is_login_form
            # Start fade out animation
            self.fade_out_animation.start()

            # Setup and start slide animation
            current_geometry = self.frameMire.geometry()
            if self.is_login_form:
                # Slide left for signup
                self.slide_animation.setStartValue(current_geometry)
                end_geometry = current_geometry.translated(-50, 0)
                self.slide_animation.setEndValue(end_geometry)
            else:
                # Slide right for login
                self.slide_animation.setStartValue(current_geometry)
                end_geometry = current_geometry.translated(50, 0)
                self.slide_animation.setEndValue(end_geometry)
            self.slide_animation.start()

    def on_fade_out_finished(self):
        """Called when fade out animation completes"""
        # Update the form state
        self.is_login_form = self.target_is_login_form
        self.update_form_state()

        # Reset position
        current_geometry = self.frameMire.geometry()
        self.frameMire.setGeometry(
            current_geometry.adjusted(50 if self.is_login_form else -50, 0, 50 if self.is_login_form else -50, 0))

        # Start fade in animation
        self.fade_in_animation.start()

        # Setup and start reverse slide animation
        self.slide_animation.setStartValue(self.frameMire.geometry())
        self.slide_animation.setEndValue(current_geometry)
        self.slide_animation.start()

    def on_fade_in_finished(self):
        """Called when fade in animation completes"""
        # Reset the opacity effect
        self.opacity_effect.setOpacity(1.0)