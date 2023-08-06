

class BuffTrajPointStream {
public:

  void * m_handle;

  void _create1() {
    m_handle = c_BuffTrajPointStream_Create1();
  }

  ~BuffTrajPointStream() {
    c_BuffTrajPointStream_Destroy(m_handle);
  }
  ctre::phoenix::ErrorCode clear() {
    
    auto __ret = c_BuffTrajPointStream_Clear(m_handle );
    return __ret;
  }


  ctre::phoenix::ErrorCode _write(double position, double velocity, double arbFeedFwd, double auxiliaryPos, double auxiliaryVel, double auxiliaryArbFeedFwd, uint32_t profileSlotSelect0, uint32_t profileSlotSelect1, bool isLastPoint, bool zeroPos, uint32_t timeDur, bool useAuxPID) {
    
    auto __ret = c_BuffTrajPointStream_Write(m_handle, position, velocity, arbFeedFwd, auxiliaryPos, auxiliaryVel, auxiliaryArbFeedFwd, profileSlotSelect0, profileSlotSelect1, isLastPoint, zeroPos, timeDur, useAuxPID );
    return __ret;
  }


};