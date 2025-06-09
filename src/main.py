import aixy
import env

if __name__ == "__main__":
    """ Large Vision Model Automonous Drive """
    env.LVMAD = True

    """ Large Languade Model Autonomous Conversations """
    env.LLMAC = True

    """ Obstacle Avoidance """
    env.OA = True

    """ Switch Between Modes """
    env.SBM = False

    """ Web Camera Stream """
    env.WCS = True

    """ Text to Speech """
    env.TTS = True

    """ Speech to Text """
    env.STT = True

    """ ONLY MANUAL CONTROL"""
    env.ONLY_MANUAL_CONTROL = False

    """ AIXY COMMANDS """
    env.COMMANDS = True

    """ Motors """
    env.MOTORS = True

    """ Camera """
    env.CAMERA = True

    """ Camera Connection """
    env.CAMERA_USB = True
    aixy.main()