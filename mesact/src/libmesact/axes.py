
from PyQt5.QtWidgets import QMessageBox

from libmesact import utilities
from libmesact import dialogs

def copy_scale(parent):
	if parent.scale_joint_cb.currentData():
		if len(parent.scale_le.text()) > 0:
			getattr(parent, f'{parent.scale_joint_cb.currentData()}').setText(parent.scale_le.text())
		else:
			msg = ('Scale must not be blank')
			dialogs.errorMsgOk(msg, 'Error')
	else:
		msg = ('Select a Joint to copy to')
		dialogs.errorMsgOk(msg, 'Error')

def copy_angular_scale(parent):
	if parent.copy_angluar_scale_cb.currentData():
		if len(parent.angular_scale_le.text()) > 0:
			getattr(parent, f'{parent.copy_angluar_scale_cb.currentData()}').setText(parent.angular_scale_le.text())
		else:
			msg = ('Scale must not be blank')
			dialogs.errorMsgOk(msg, 'Error')
	else:
		msg = ('Select a Joint to copy to')
		dialogs.errorMsgOk(msg, 'Error')


def axisChanged(parent):
	if parent.sender().currentData():
		connector = parent.sender().objectName()[:3]
		joint = parent.sender().objectName()[-1]
		axis = parent.sender().currentText()
		linear_axes = ['X', 'Y', 'Z', 'U', 'V', 'W']
		angular_axes = ['A', 'B', 'C']
		if axis in linear_axes:
			getattr(parent, f'{connector}axisType_{joint}').setText('LINEAR')
			parent.minAngJogVelDSB.setEnabled(False)
			parent.defAngJogVelDSB.setEnabled(False)
			parent.maxAngJogVelDSB.setEnabled(False)
		elif axis in angular_axes:
			getattr(parent, f'{connector}axisType_{joint}').setText('ANGULAR')
			parent.minAngJogVelDSB.setEnabled(True)
			parent.defAngJogVelDSB.setEnabled(True)
			parent.maxAngJogVelDSB.setEnabled(True)
		else:
			getattr(parent, f'{connector}axisType_{joint}').setText('')
			parent.minAngJogVelDSB.setEnabled(False)
			parent.defAngJogVelDSB.setEnabled(False)
			parent.maxAngJogVelDSB.setEnabled(False)
		coordList = []

		parent.scale_joint_cb.clear()
		parent.scale_joint_cb.addItem('Select', False)
		parent.copy_angluar_scale_cb.clear()
		parent.copy_angluar_scale_cb.addItem('Select', False)
		for i in range(3):
			for j in range(6):
				axis_letter = getattr(parent, f'c{i}_axis_{j}').currentText()
				if axis_letter != 'Select':
					coordList.append(axis_letter)
					if axis_letter in linear_axes:
						parent.scale_joint_cb.addItem(f'Axis {axis_letter} Joint {j} ', f'c{i}_scale_{j}')
					elif axis_letter in angular_axes:
						parent.copy_angluar_scale_cb.addItem(f'Axis {axis_letter} Joint {j} ', f'c{i}_scale_{j}')
				parent.coordinatesLB.setText(''.join(coordList))
		if coordList:
			parent.copy_scale_pb.setEnabled(True)
			parent.copy_angluar_scale_pb.setEnabled(True)
		else:
			parent.copy_scale_pb.setEnabled(False)
			parent.copy_angluar_scale_pb.setEnabled(False)
			parent.scale_joint_cb.clear()
			parent.copy_angluar_scale_cb.clear()


def updateAxisInfo(parent):
	card = parent.sender().objectName()[:2]
	joint = parent.sender().objectName()[-1]
	scale = getattr(parent, f'{card}_scale_' + joint).text()
	if scale and utilities.is_number(scale):
		scale = float(scale)
	else:
		return

	maxVelocity = getattr(parent, f'{card}_max_vel_' + joint).text()
	if maxVelocity and utilities.is_number(maxVelocity):
		maxVelocity = float(maxVelocity)
	else:
		return

	maxAccel = getattr(parent, f'{card}_max_accel_' + joint).text()
	if maxAccel and utilities.is_number(maxAccel):
		maxAccel = float(maxAccel)
	else:
		return

	if parent.linearUnitsCB.currentData():
		accelTime = maxVelocity / maxAccel
		getattr(parent, f'{card}_timeJoint_' + joint).setText(f'{accelTime:.3f} seconds')
		accelDistance = accelTime * 0.5 * maxVelocity
		getattr(parent, f'{card}_distanceJoint_' + joint).setText(f'{accelDistance:.3f} {parent.linearUnitsCB.currentData()}')
		stepRate = scale * maxVelocity
		getattr(parent, f'{card}_stepRateJoint_' + joint).setText(f'{abs(stepRate):.0f} Hz')

def pidSetDefault(parent):
	connector = parent.sender().objectName()[:2]
	joint = parent.sender().objectName()[-1]
	if not parent.linearUnitsCB.currentData():
		QMessageBox.warning(parent,'Warning', 'Settings Tab\nLinear Units\nmust be selected', QMessageBox.Ok)
		return
	if joint == 's':
		getattr(parent, 'p_s').setValue(0)
		getattr(parent, 'i_s').setValue(0)
		getattr(parent, 'd_s').setValue(0)
		getattr(parent, 'ff0_s').setValue(1)
		getattr(parent, 'ff1_s').setValue(0)
		getattr(parent, 'ff2_s').setValue(0)
		getattr(parent, 'bias_s').setValue(0)
		getattr(parent, 'maxOutput_s').setValue(parent.spindleMaxRpm.value())
		getattr(parent, 'maxError_s').setValue(0)
		getattr(parent, 'deadband_s').setValue(0)
		return

	p = int(1000/(parent.servoPeriodSB.value()/1000000))
	getattr(parent,  f'{connector}_p_{joint}').setText(f'{p}')
	getattr(parent, f'{connector}_i_{joint}').setText('0')
	getattr(parent, f'{connector}_d_{joint}').setText('0')
	getattr(parent, f'{connector}_ff0_{joint}').setText('0')
	getattr(parent, f'{connector}_ff1_{joint}').setText('1')
	getattr(parent, f'{connector}_ff2_{joint}').setText('0')
	getattr(parent, f'{connector}_bias_{joint}').setText('0')
	getattr(parent, f'{connector}_maxOutput_{joint}').setText('0')
	if parent.linearUnitsCB.itemData(parent.linearUnitsCB.currentIndex()) == 'inch':
		maxError = '0.0005'
	else:
		maxError = '0.0127'
	getattr(parent, f'{connector}_maxError_{joint}').setText(maxError)
	getattr(parent, f'{connector}_deadband_{joint}').setText('0')

def ferrorSetDefault(parent):
	if not parent.linearUnitsCB.currentData():
		QMessageBox.warning(parent,'Warning', 'Machine Tab\nLinear Units\nmust be selected', QMessageBox.Ok)
		return
	connector = parent.sender().objectName()[:2]
	joint = parent.sender().objectName()[-1]
	if parent.linearUnitsCB.currentData() == 'inch':
		getattr(parent, f'{connector}_max_ferror_{joint}').setText(' 0.002')
		getattr(parent, f'{connector}_min_ferror_{joint}').setText(' 0.001')
	else:
		getattr(parent, f'{connector}_max_ferror_{joint}').setText(' 0.005')
		getattr(parent, f'{connector}_min_ferror_{joint}').setText(' 0.0025')

def analogSetDefault(parent):
	connector = parent.sender().objectName()[:2]
	joint = parent.sender().objectName()[-1]
	getattr(parent, f'{connector}_analogMinLimit_{joint}').setText('-10')
	getattr(parent, f'{connector}_analogMaxLimit_{joint}').setText('10')
	getattr(parent, f'{connector}_analogScaleMax_{joint}').setText('10')

def driveChanged(parent):
	timing = parent.sender().currentData()
	connector = parent.sender().objectName()[:3]
	joint = f'_{parent.sender().objectName()[-1]}'
	if parent.sender().objectName() == 'spindleDriveCB':
		connector = 'spindle'
		joint = ''
	if timing:
		parent.sender().setEditable(False)
		getattr(parent, f'{connector}StepTime{joint}').setText(timing[0])
		getattr(parent, f'{connector}StepSpace{joint}').setText(timing[1])
		getattr(parent, f'{connector}DirSetup{joint}').setText(timing[2])
		getattr(parent, f'{connector}DirHold{joint}').setText(timing[3])
		getattr(parent, f'{connector}StepTime{joint}').setEnabled(False)
		getattr(parent, f'{connector}StepSpace{joint}').setEnabled(False)
		getattr(parent, f'{connector}DirSetup{joint}').setEnabled(False)
		getattr(parent, f'{connector}DirHold{joint}').setEnabled(False)
	else:
		parent.sender().setEditable(True)
		getattr(parent, f'{connector}StepTime{joint}').setEnabled(True)
		getattr(parent, f'{connector}StepSpace{joint}').setEnabled(True)
		getattr(parent, f'{connector}DirSetup{joint}').setEnabled(True)
		getattr(parent, f'{connector}DirHold{joint}').setEnabled(True)

def spindleTypeChanged(parent):
	connector = parent.sender().objectName()[1:2]
	if parent.sender().currentData():
		getattr(parent, f'c{connector}_spindle_pwm_freq').setEnabled(True)
		getattr(parent, f'c{connector}_spindle_encoder').setEnabled(True)
	else:
		getattr(parent, f'c{connector}_spindle_pwm_freq').setEnabled(False)
		getattr(parent, f'c{connector}_spindle_encoder').setCurrentIndex(0)
		getattr(parent, f'c{connector}_spindle_encoder').setEnabled(False)
		getattr(parent, f'c{connector}_spindle_scale').setEnabled(False)

def spindleEncoderChanged(parent):
	connector = parent.sender().objectName()[1:2]
	if parent.sender().currentData():
		getattr(parent, f'c{connector}_spindle_scale').setEnabled(True)
	else:
		getattr(parent, f'c{connector}_spindle_scale').setEnabled(False)


