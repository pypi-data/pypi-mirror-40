

class MotController {
public:

  void * m_handle;

  void _create1(int baseArbId) {
    m_handle = c_MotController_Create1(baseArbId);
  }

  ~MotController() {
    c_MotController_Destroy(m_handle);
  }
  int getDeviceNumber() {
    int deviceNumber;
     c_MotController_GetDeviceNumber(m_handle, &deviceNumber );
    return deviceNumber;
  }


  ctre::phoenix::ErrorCode setDemand(int mode, int demand0, int demand1) {
    
    auto __ret = c_MotController_SetDemand(m_handle, mode, demand0, demand1 );
    return __ret;
  }


  ctre::phoenix::ErrorCode _set_4(int mode, double demand0, double demand1, int demand1Type) {
    
    auto __ret = c_MotController_Set_4(m_handle, mode, demand0, demand1, demand1Type );
    return __ret;
  }


  void setNeutralMode(int neutralMode) {
    
     c_MotController_SetNeutralMode(m_handle, neutralMode );
    
  }


  void setSensorPhase(bool PhaseSensor) {
    
     c_MotController_SetSensorPhase(m_handle, PhaseSensor );
    
  }


  void _setInverted_2(int invertType) {
    
     c_MotController_SetInverted_2(m_handle, invertType );
    
  }


  ctre::phoenix::ErrorCode configFactoryDefault(int timeoutMs) {
    
    auto __ret = c_MotController_ConfigFactoryDefault(m_handle, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode configOpenLoopRamp(double secondsFromNeutralToFull, int timeoutMs) {
    
    auto __ret = c_MotController_ConfigOpenLoopRamp(m_handle, secondsFromNeutralToFull, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode configClosedLoopRamp(double secondsFromNeutralToFull, int timeoutMs) {
    
    auto __ret = c_MotController_ConfigClosedLoopRamp(m_handle, secondsFromNeutralToFull, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode configPeakOutputForward(double percentOut, int timeoutMs) {
    
    auto __ret = c_MotController_ConfigPeakOutputForward(m_handle, percentOut, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode configPeakOutputReverse(double percentOut, int timeoutMs) {
    
    auto __ret = c_MotController_ConfigPeakOutputReverse(m_handle, percentOut, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode configNominalOutputForward(double percentOut, int timeoutMs) {
    
    auto __ret = c_MotController_ConfigNominalOutputForward(m_handle, percentOut, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode configNominalOutputReverse(double percentOut, int timeoutMs) {
    
    auto __ret = c_MotController_ConfigNominalOutputReverse(m_handle, percentOut, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode configNeutralDeadband(double percentDeadband, int timeoutMs) {
    
    auto __ret = c_MotController_ConfigNeutralDeadband(m_handle, percentDeadband, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode configVoltageCompSaturation(double voltage, int timeoutMs) {
    
    auto __ret = c_MotController_ConfigVoltageCompSaturation(m_handle, voltage, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode configVoltageMeasurementFilter(int filterWindowSamples, int timeoutMs) {
    
    auto __ret = c_MotController_ConfigVoltageMeasurementFilter(m_handle, filterWindowSamples, timeoutMs );
    return __ret;
  }


  void enableVoltageCompensation(bool enable) {
    
     c_MotController_EnableVoltageCompensation(m_handle, enable );
    
  }


  bool getInverted() {
    bool invert;
     c_MotController_GetInverted(m_handle, &invert );
    return invert;
  }


  double getBusVoltage() {
    double voltage;
     c_MotController_GetBusVoltage(m_handle, &voltage );
    return voltage;
  }


  double getMotorOutputPercent() {
    double percentOutput;
     c_MotController_GetMotorOutputPercent(m_handle, &percentOutput );
    return percentOutput;
  }


  double getOutputCurrent() {
    double current;
     c_MotController_GetOutputCurrent(m_handle, &current );
    return current;
  }


  double getTemperature() {
    double temperature;
     c_MotController_GetTemperature(m_handle, &temperature );
    return temperature;
  }


  ctre::phoenix::ErrorCode configSelectedFeedbackSensor(int feedbackDevice, int pidIdx, int timeoutMs) {
    
    auto __ret = c_MotController_ConfigSelectedFeedbackSensor(m_handle, feedbackDevice, pidIdx, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode configSelectedFeedbackCoefficient(double coefficient, int pidIdx, int timeoutMs) {
    
    auto __ret = c_MotController_ConfigSelectedFeedbackCoefficient(m_handle, coefficient, pidIdx, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode configRemoteFeedbackFilter(int deviceID, int remoteSensorSource, int remoteOrdinal, int timeoutMs) {
    
    auto __ret = c_MotController_ConfigRemoteFeedbackFilter(m_handle, deviceID, remoteSensorSource, remoteOrdinal, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode configSensorTerm(int sensorTerm, int feedbackDevice, int timeoutMs) {
    
    auto __ret = c_MotController_ConfigSensorTerm(m_handle, sensorTerm, feedbackDevice, timeoutMs );
    return __ret;
  }


  int getSelectedSensorPosition(int pidIdx) {
    int param;
     c_MotController_GetSelectedSensorPosition(m_handle, &param, pidIdx );
    return param;
  }


  int getSelectedSensorVelocity(int pidIdx) {
    int param;
     c_MotController_GetSelectedSensorVelocity(m_handle, &param, pidIdx );
    return param;
  }


  ctre::phoenix::ErrorCode setSelectedSensorPosition(int sensorPos, int pidIdx, int timeoutMs) {
    
    auto __ret = c_MotController_SetSelectedSensorPosition(m_handle, sensorPos, pidIdx, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode setControlFramePeriod(int frame, int periodMs) {
    
    auto __ret = c_MotController_SetControlFramePeriod(m_handle, frame, periodMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode setStatusFramePeriod(int frame, uint8_t periodMs, int timeoutMs) {
    
    auto __ret = c_MotController_SetStatusFramePeriod(m_handle, frame, periodMs, timeoutMs );
    return __ret;
  }


  int getStatusFramePeriod(int frame, int timeoutMs) {
    int periodMs;
     c_MotController_GetStatusFramePeriod(m_handle, frame, &periodMs, timeoutMs );
    return periodMs;
  }


  ctre::phoenix::ErrorCode configVelocityMeasurementPeriod(int period, int timeoutMs) {
    
    auto __ret = c_MotController_ConfigVelocityMeasurementPeriod(m_handle, period, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode configVelocityMeasurementWindow(int windowSize, int timeoutMs) {
    
    auto __ret = c_MotController_ConfigVelocityMeasurementWindow(m_handle, windowSize, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode configForwardLimitSwitchSource(int type, int normalOpenOrClose, int deviceID, int timeoutMs) {
    
    auto __ret = c_MotController_ConfigForwardLimitSwitchSource(m_handle, type, normalOpenOrClose, deviceID, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode configReverseLimitSwitchSource(int type, int normalOpenOrClose, int deviceID, int timeoutMs) {
    
    auto __ret = c_MotController_ConfigReverseLimitSwitchSource(m_handle, type, normalOpenOrClose, deviceID, timeoutMs );
    return __ret;
  }


  void overrideLimitSwitchesEnable(bool enable) {
    
     c_MotController_OverrideLimitSwitchesEnable(m_handle, enable );
    
  }


  ctre::phoenix::ErrorCode configForwardSoftLimitThreshold(int forwardSensorLimit, int timeoutMs) {
    
    auto __ret = c_MotController_ConfigForwardSoftLimitThreshold(m_handle, forwardSensorLimit, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode configReverseSoftLimitThreshold(int reverseSensorLimit, int timeoutMs) {
    
    auto __ret = c_MotController_ConfigReverseSoftLimitThreshold(m_handle, reverseSensorLimit, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode configForwardSoftLimitEnable(bool enable, int timeoutMs) {
    
    auto __ret = c_MotController_ConfigForwardSoftLimitEnable(m_handle, enable, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode configReverseSoftLimitEnable(bool enable, int timeoutMs) {
    
    auto __ret = c_MotController_ConfigReverseSoftLimitEnable(m_handle, enable, timeoutMs );
    return __ret;
  }


  void overrideSoftLimitsEnable(bool enable) {
    
     c_MotController_OverrideSoftLimitsEnable(m_handle, enable );
    
  }


  ctre::phoenix::ErrorCode config_kP(int slotIdx, double value, int timeoutMs) {
    
    auto __ret = c_MotController_Config_kP(m_handle, slotIdx, value, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode config_kI(int slotIdx, double value, int timeoutMs) {
    
    auto __ret = c_MotController_Config_kI(m_handle, slotIdx, value, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode config_kD(int slotIdx, double value, int timeoutMs) {
    
    auto __ret = c_MotController_Config_kD(m_handle, slotIdx, value, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode config_kF(int slotIdx, double value, int timeoutMs) {
    
    auto __ret = c_MotController_Config_kF(m_handle, slotIdx, value, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode config_IntegralZone(int slotIdx, double izone, int timeoutMs) {
    
    auto __ret = c_MotController_Config_IntegralZone(m_handle, slotIdx, izone, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode configAllowableClosedloopError(int slotIdx, int allowableClosedLoopError, int timeoutMs) {
    
    auto __ret = c_MotController_ConfigAllowableClosedloopError(m_handle, slotIdx, allowableClosedLoopError, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode configMaxIntegralAccumulator(int slotIdx, double iaccum, int timeoutMs) {
    
    auto __ret = c_MotController_ConfigMaxIntegralAccumulator(m_handle, slotIdx, iaccum, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode configClosedLoopPeakOutput(int slotIdx, double percentOut, int timeoutMs) {
    
    auto __ret = c_MotController_ConfigClosedLoopPeakOutput(m_handle, slotIdx, percentOut, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode configClosedLoopPeriod(int slotIdx, int loopTimeMs, int timeoutMs) {
    
    auto __ret = c_MotController_ConfigClosedLoopPeriod(m_handle, slotIdx, loopTimeMs, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode setIntegralAccumulator(double iaccum, int pidIdx, int timeoutMs) {
    
    auto __ret = c_MotController_SetIntegralAccumulator(m_handle, iaccum, pidIdx, timeoutMs );
    return __ret;
  }


  int getClosedLoopError(int pidIdx) {
    int closedLoopError;
     c_MotController_GetClosedLoopError(m_handle, &closedLoopError, pidIdx );
    return closedLoopError;
  }


  double getIntegralAccumulator(int pidIdx) {
    double iaccum;
     c_MotController_GetIntegralAccumulator(m_handle, &iaccum, pidIdx );
    return iaccum;
  }


  double getErrorDerivative(int pidIdx) {
    double derror;
     c_MotController_GetErrorDerivative(m_handle, &derror, pidIdx );
    return derror;
  }


  ctre::phoenix::ErrorCode selectProfileSlot(int slotIdx, int pidIdx) {
    
    auto __ret = c_MotController_SelectProfileSlot(m_handle, slotIdx, pidIdx );
    return __ret;
  }


  double getActiveTrajectoryHeading() {
    double param;
     c_MotController_GetActiveTrajectoryHeading(m_handle, &param );
    return param;
  }


  int getActiveTrajectoryPosition(int pidIdx) {
    int param;
     c_MotController_GetActiveTrajectoryPosition_3(m_handle, &param, pidIdx );
    return param;
  }


  int getActiveTrajectoryVelocity(int pidIdx) {
    int param;
     c_MotController_GetActiveTrajectoryVelocity_3(m_handle, &param, pidIdx );
    return param;
  }


  double getActiveTrajectoryArbFeedFwd(int pidIdx) {
    double param;
     c_MotController_GetActiveTrajectoryArbFeedFwd_3(m_handle, &param, pidIdx );
    return param;
  }


  std::tuple<int, int, double> getActiveTrajectoryAll(int pidIdx) {
    int vel;int pos;double arbFeedFwd;
     c_MotController_GetActiveTrajectoryAll_5(m_handle, &vel, &pos, &arbFeedFwd, pidIdx );
    return std::make_tuple(vel,pos,arbFeedFwd);
  }


  ctre::phoenix::ErrorCode configMotionCruiseVelocity(int sensorUnitsPer100ms, int timeoutMs) {
    
    auto __ret = c_MotController_ConfigMotionCruiseVelocity(m_handle, sensorUnitsPer100ms, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode configMotionAcceleration(int sensorUnitsPer100msPerSec, int timeoutMs) {
    
    auto __ret = c_MotController_ConfigMotionAcceleration(m_handle, sensorUnitsPer100msPerSec, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode clearMotionProfileTrajectories() {
    
    auto __ret = c_MotController_ClearMotionProfileTrajectories(m_handle );
    return __ret;
  }


  int getMotionProfileTopLevelBufferCount() {
    int value;
     c_MotController_GetMotionProfileTopLevelBufferCount(m_handle, &value );
    return value;
  }


  ctre::phoenix::ErrorCode _pushMotionProfileTrajectory(double position, double velocity, double headingDeg, int profileSlotSelect, bool isLastPoint, bool zeroPos) {
    
    auto __ret = c_MotController_PushMotionProfileTrajectory(m_handle, position, velocity, headingDeg, profileSlotSelect, isLastPoint, zeroPos );
    return __ret;
  }


  ctre::phoenix::ErrorCode _pushMotionProfileTrajectory_2(double position, double velocity, double headingDeg, int profileSlotSelect0, int profileSlotSelect1, bool isLastPoint, bool zeroPos, int durationMs) {
    
    auto __ret = c_MotController_PushMotionProfileTrajectory_2(m_handle, position, velocity, headingDeg, profileSlotSelect0, profileSlotSelect1, isLastPoint, zeroPos, durationMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode _pushMotionProfileTrajectory_3(double position, double velocity, double arbFeedFwd, double auxiliaryPos, double auxiliaryVel, double auxiliaryArbFeedFwd, uint32_t profileSlotSelect0, uint32_t profileSlotSelect1, bool isLastPoint, bool zeroPos0, uint32_t timeDur, bool useAuxPID) {
    
    auto __ret = c_MotController_PushMotionProfileTrajectory_3(m_handle, position, velocity, arbFeedFwd, auxiliaryPos, auxiliaryVel, auxiliaryArbFeedFwd, profileSlotSelect0, profileSlotSelect1, isLastPoint, zeroPos0, timeDur, useAuxPID );
    return __ret;
  }


  ctre::phoenix::ErrorCode startMotionProfile(BuffTrajPointStream& stream, uint32_t minBufferedPts, ctre::phoenix::motorcontrol::ControlMode controlMode) {
    
    auto __ret = c_MotController_StartMotionProfile(m_handle, stream.m_handle, minBufferedPts, controlMode );
    return __ret;
  }


  bool isMotionProfileFinished() {
    bool value;
     c_MotController_IsMotionProfileFinished(m_handle, &value );
    return value;
  }


  bool isMotionProfileTopLevelBufferFull() {
    bool value;
     c_MotController_IsMotionProfileTopLevelBufferFull(m_handle, &value );
    return value;
  }


  ctre::phoenix::ErrorCode processMotionProfileBuffer() {
    
    auto __ret = c_MotController_ProcessMotionProfileBuffer(m_handle );
    return __ret;
  }


  std::tuple<size_t, size_t, int, bool, bool, bool, bool, int, int> _getMotionProfileStatus() {
    size_t topBufferRem;size_t topBufferCnt;int btmBufferCnt;bool hasUnderrun;bool isUnderrun;bool activePointValid;bool isLast;int profileSlotSelect;int outputEnable;
     c_MotController_GetMotionProfileStatus(m_handle, &topBufferRem, &topBufferCnt, &btmBufferCnt, &hasUnderrun, &isUnderrun, &activePointValid, &isLast, &profileSlotSelect, &outputEnable );
    return std::make_tuple(topBufferRem,topBufferCnt,btmBufferCnt,hasUnderrun,isUnderrun,activePointValid,isLast,profileSlotSelect,outputEnable);
  }


  std::tuple<size_t, size_t, int, bool, bool, bool, bool, int, int, int, int> _getMotionProfileStatus_2() {
    size_t topBufferRem;size_t topBufferCnt;int btmBufferCnt;bool hasUnderrun;bool isUnderrun;bool activePointValid;bool isLast;int profileSlotSelect;int outputEnable;int timeDurMs;int profileSlotSelect1;
     c_MotController_GetMotionProfileStatus_2(m_handle, &topBufferRem, &topBufferCnt, &btmBufferCnt, &hasUnderrun, &isUnderrun, &activePointValid, &isLast, &profileSlotSelect, &outputEnable, &timeDurMs, &profileSlotSelect1 );
    return std::make_tuple(topBufferRem,topBufferCnt,btmBufferCnt,hasUnderrun,isUnderrun,activePointValid,isLast,profileSlotSelect,outputEnable,timeDurMs,profileSlotSelect1);
  }


  ctre::phoenix::ErrorCode clearMotionProfileHasUnderrun(int timeoutMs) {
    
    auto __ret = c_MotController_ClearMotionProfileHasUnderrun(m_handle, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode changeMotionControlFramePeriod(int periodMs) {
    
    auto __ret = c_MotController_ChangeMotionControlFramePeriod(m_handle, periodMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode configMotionProfileTrajectoryPeriod(int durationMs, int timeoutMs) {
    
    auto __ret = c_MotController_ConfigMotionProfileTrajectoryPeriod(m_handle, durationMs, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode configMotionProfileTrajectoryInterpolationEnable(bool enable, int timeoutMs) {
    
    auto __ret = c_MotController_ConfigMotionProfileTrajectoryInterpolationEnable(m_handle, enable, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode configFeedbackNotContinuous(bool feedbackNotContinuous, int timeoutMs) {
    
    auto __ret = c_MotController_ConfigFeedbackNotContinuous(m_handle, feedbackNotContinuous, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode configRemoteSensorClosedLoopDisableNeutralOnLOS(bool remoteSensorClosedLoopDisableNeutralOnLOS, int timeoutMs) {
    
    auto __ret = c_MotController_ConfigRemoteSensorClosedLoopDisableNeutralOnLOS(m_handle, remoteSensorClosedLoopDisableNeutralOnLOS, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode configClearPositionOnLimitF(bool clearPositionOnLimitF, int timeoutMs) {
    
    auto __ret = c_MotController_ConfigClearPositionOnLimitF(m_handle, clearPositionOnLimitF, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode configClearPositionOnLimitR(bool clearPositionOnLimitR, int timeoutMs) {
    
    auto __ret = c_MotController_ConfigClearPositionOnLimitR(m_handle, clearPositionOnLimitR, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode configClearPositionOnQuadIdx(bool clearPositionOnQuadIdx, int timeoutMs) {
    
    auto __ret = c_MotController_ConfigClearPositionOnQuadIdx(m_handle, clearPositionOnQuadIdx, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode configLimitSwitchDisableNeutralOnLOS(bool limitSwitchDisableNeutralOnLOS, int timeoutMs) {
    
    auto __ret = c_MotController_ConfigLimitSwitchDisableNeutralOnLOS(m_handle, limitSwitchDisableNeutralOnLOS, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode configSoftLimitDisableNeutralOnLOS(bool softLimitDisableNeutralOnLOS, int timeoutMs) {
    
    auto __ret = c_MotController_ConfigSoftLimitDisableNeutralOnLOS(m_handle, softLimitDisableNeutralOnLOS, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode configPulseWidthPeriod_EdgesPerRot(int pulseWidthPeriod_EdgesPerRot, int timeoutMs) {
    
    auto __ret = c_MotController_ConfigPulseWidthPeriod_EdgesPerRot(m_handle, pulseWidthPeriod_EdgesPerRot, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode configPulseWidthPeriod_FilterWindowSz(int pulseWidthPeriod_FilterWindowSz, int timeoutMs) {
    
    auto __ret = c_MotController_ConfigPulseWidthPeriod_FilterWindowSz(m_handle, pulseWidthPeriod_FilterWindowSz, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode getLastError() {
    
    auto __ret = c_MotController_GetLastError(m_handle );
    return __ret;
  }


  int getFirmwareVersion() {
    int param0;
     c_MotController_GetFirmwareVersion(m_handle, &param0 );
    return param0;
  }


  bool hasResetOccurred() {
    bool param0;
     c_MotController_HasResetOccurred(m_handle, &param0 );
    return param0;
  }


  ctre::phoenix::ErrorCode configSetCustomParam(int newValue, int paramIndex, int timeoutMs) {
    
    auto __ret = c_MotController_ConfigSetCustomParam(m_handle, newValue, paramIndex, timeoutMs );
    return __ret;
  }


  int configGetCustomParam(int paramIndex, int timoutMs) {
    int readValue;
     c_MotController_ConfigGetCustomParam(m_handle, &readValue, paramIndex, timoutMs );
    return readValue;
  }


  ctre::phoenix::ErrorCode configSetParameter(int param, double value, uint8_t subValue, int ordinal, int timeoutMs) {
    
    auto __ret = c_MotController_ConfigSetParameter(m_handle, param, value, subValue, ordinal, timeoutMs );
    return __ret;
  }


  double configGetParameter(int param, int ordinal, int timeoutMs) {
    double value;
     c_MotController_ConfigGetParameter(m_handle, param, &value, ordinal, timeoutMs );
    return value;
  }


  std::tuple<int32_t, uint8_t> configGetParameter_6(int32_t param, int32_t valueToSend, int32_t ordinal, int32_t timeoutMs) {
    int32_t valueRecieved;uint8_t subValue;
     c_MotController_ConfigGetParameter_6(m_handle, param, valueToSend, &valueRecieved, &subValue, ordinal, timeoutMs );
    return std::make_tuple(valueRecieved,subValue);
  }


  ctre::phoenix::ErrorCode configPeakCurrentLimit(int amps, int timeoutMs) {
    
    auto __ret = c_MotController_ConfigPeakCurrentLimit(m_handle, amps, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode configPeakCurrentDuration(int milliseconds, int timeoutMs) {
    
    auto __ret = c_MotController_ConfigPeakCurrentDuration(m_handle, milliseconds, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode configContinuousCurrentLimit(int amps, int timeoutMs) {
    
    auto __ret = c_MotController_ConfigContinuousCurrentLimit(m_handle, amps, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode enableCurrentLimit(bool enable) {
    
    auto __ret = c_MotController_EnableCurrentLimit(m_handle, enable );
    return __ret;
  }


  ctre::phoenix::ErrorCode setLastError(int error) {
    
    auto __ret = c_MotController_SetLastError(m_handle, error );
    return __ret;
  }


  int getAnalogIn() {
    int param;
     c_MotController_GetAnalogIn(m_handle, &param );
    return param;
  }


  ctre::phoenix::ErrorCode setAnalogPosition(int newPosition, int timeoutMs) {
    
    auto __ret = c_MotController_SetAnalogPosition(m_handle, newPosition, timeoutMs );
    return __ret;
  }


  int getAnalogInRaw() {
    int param;
     c_MotController_GetAnalogInRaw(m_handle, &param );
    return param;
  }


  int getAnalogInVel() {
    int param;
     c_MotController_GetAnalogInVel(m_handle, &param );
    return param;
  }


  int getQuadraturePosition() {
    int param;
     c_MotController_GetQuadraturePosition(m_handle, &param );
    return param;
  }


  ctre::phoenix::ErrorCode setQuadraturePosition(int newPosition, int timeoutMs) {
    
    auto __ret = c_MotController_SetQuadraturePosition(m_handle, newPosition, timeoutMs );
    return __ret;
  }


  int getQuadratureVelocity() {
    int param;
     c_MotController_GetQuadratureVelocity(m_handle, &param );
    return param;
  }


  int getPulseWidthPosition() {
    int param;
     c_MotController_GetPulseWidthPosition(m_handle, &param );
    return param;
  }


  ctre::phoenix::ErrorCode setPulseWidthPosition(int newPosition, int timeoutMs) {
    
    auto __ret = c_MotController_SetPulseWidthPosition(m_handle, newPosition, timeoutMs );
    return __ret;
  }


  int getPulseWidthVelocity() {
    int param;
     c_MotController_GetPulseWidthVelocity(m_handle, &param );
    return param;
  }


  int getPulseWidthRiseToFallUs() {
    int param;
     c_MotController_GetPulseWidthRiseToFallUs(m_handle, &param );
    return param;
  }


  int getPulseWidthRiseToRiseUs() {
    int param;
     c_MotController_GetPulseWidthRiseToRiseUs(m_handle, &param );
    return param;
  }


  int getPinStateQuadA() {
    int param;
     c_MotController_GetPinStateQuadA(m_handle, &param );
    return param;
  }


  int getPinStateQuadB() {
    int param;
     c_MotController_GetPinStateQuadB(m_handle, &param );
    return param;
  }


  int getPinStateQuadIdx() {
    int param;
     c_MotController_GetPinStateQuadIdx(m_handle, &param );
    return param;
  }


  int isFwdLimitSwitchClosed() {
    int param;
     c_MotController_IsFwdLimitSwitchClosed(m_handle, &param );
    return param;
  }


  int isRevLimitSwitchClosed() {
    int param;
     c_MotController_IsRevLimitSwitchClosed(m_handle, &param );
    return param;
  }


  int _getFaults() {
    int param;
     c_MotController_GetFaults(m_handle, &param );
    return param;
  }


  int _getStickyFaults() {
    int param;
     c_MotController_GetStickyFaults(m_handle, &param );
    return param;
  }


  ctre::phoenix::ErrorCode clearStickyFaults(int timeoutMs) {
    
    auto __ret = c_MotController_ClearStickyFaults(m_handle, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode selectDemandType(bool enable) {
    
    auto __ret = c_MotController_SelectDemandType(m_handle, enable );
    return __ret;
  }


  ctre::phoenix::ErrorCode setMPEOutput(int MpeOutput) {
    
    auto __ret = c_MotController_SetMPEOutput(m_handle, MpeOutput );
    return __ret;
  }


  ctre::phoenix::ErrorCode enableHeadingHold(bool enable) {
    
    auto __ret = c_MotController_EnableHeadingHold(m_handle, enable );
    return __ret;
  }


  std::tuple<int, int, int> getAnalogInAll() {
    int withOv;int raw;int vel;
     c_MotController_GetAnalogInAll(m_handle, &withOv, &raw, &vel );
    return std::make_tuple(withOv,raw,vel);
  }


  std::tuple<int, int> getQuadratureSensor() {
    int pos;int vel;
     c_MotController_GetQuadratureSensor(m_handle, &pos, &vel );
    return std::make_tuple(pos,vel);
  }


  std::tuple<int, int, int, int> getPulseWidthAll() {
    int pos;int vel;int riseToRiseUs;int riseToFallUs;
     c_MotController_GetPulseWidthAll(m_handle, &pos, &vel, &riseToRiseUs, &riseToFallUs );
    return std::make_tuple(pos,vel,riseToRiseUs,riseToFallUs);
  }


  std::tuple<int, int, int> getQuadPinStates() {
    int quadA;int quadB;int quadIdx;
     c_MotController_GetQuadPinStates(m_handle, &quadA, &quadB, &quadIdx );
    return std::make_tuple(quadA,quadB,quadIdx);
  }


  std::tuple<int, int> getLimitSwitchState() {
    int isFwdClosed;int isRevClosed;
     c_MotController_GetLimitSwitchState(m_handle, &isFwdClosed, &isRevClosed );
    return std::make_tuple(isFwdClosed,isRevClosed);
  }


  int getClosedLoopTarget(int pidIdx) {
    int value;
     c_MotController_GetClosedLoopTarget(m_handle, &value, pidIdx );
    return value;
  }


};