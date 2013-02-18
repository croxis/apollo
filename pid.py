class PID:
	def __init__ (self):
		self.Reset ()


	def __str__ (self):
		return 'p: %f, i: %f, d: %f' % (self.P, self.I, self.D)


	def GetKp (self):
		return self.__Kp
	def SetKp (self, value):
		self.__Kp = value
	Kp = property (GetKp, SetKp)

	def GetKi (self):
		return self.__Ki
	def SetKi (self, value):
		self.__Ki = value
	Ki = property (GetKi, SetKi)

	def GetKd (self):
		return self.__Kd
	def SetKd (self, value):
		self.__Kd = value
	Kd = property (GetKd, SetKd)

	def GetIMin (self):
		return self.__iMin
	def SetIMin (self, value):
		self.__iMin = value
	IMin = property (GetIMin, SetIMin)

	def GetIMax (self):
		return self.__iMax
	def SetIMax (self, value):
		self.__iMax = value
	IMax = property (GetIMax, SetIMax)

	def GetUseP (self):
		return self.__useP
	def SetUseP (self, value):
		self.__useP = value
	UseP = property (GetUseP, SetUseP)

	def GetUseI (self):
		return self.__useI
	def SetUseI (self, value):
		self.__useI = value
	UseI = property (GetUseI, SetUseI)

	def GetUseD (self):
		return self.__useD
	def SetUseD (self, value):
		self.__useD = value
	UseD = property (GetUseD, SetUseD)

	def GetP (self):
		return self.__p
	P = property (GetP)

	def GetI (self):
		return self.__i
	I = property (GetI)

	def GetD (self):
		return self.__d
	D = property (GetD)


	def Reset (self):
		self.__Kp = 1.0
		self.__Ki = 1.0
		self.__Kd = 1.0
		self.__iMin = 0.0
		self.__iMax = 1.0
		self.__iState = 0.0
		self.__dState = 0.0
		self.__p = 0.0
		self.__i = 0.0
		self.__d = 0.0
		self.__useP = True
		self.__useI = True
		self.__useD = True


	def Update (self, error, position):
		self.UpdateP (error, position)
		self.UpdateI (error, position)
		self.UpdateD (error, position)
		return self.GetControlValue ()


	def GetControlValue (self):
		result = 0.0
		if self.UseP:
			result += self.P
		if self.UseI:
			result += self.I
		if self.UseD:
			result -= self.D
		return result


	def UpdateP (self, error, position=0):
		self.P = self.Kp * error
		return self.P


	def UpdateI (self, error, position=0):
		self.__iState += error
		if self.__iState > self.IMax:
			self.__iState = self.IMax
		elif self.__iState < self.IMin:
			self.__iState = self.IMin
		self.I = self.Ki * self.__iState
		return self.I


	def UpdateD (self, error, position):
		self.D = self.Kd * (position - self.__dState)
		self.__dState = position
		return self.D
