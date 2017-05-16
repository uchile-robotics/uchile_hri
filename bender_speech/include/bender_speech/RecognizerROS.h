#ifndef RECOGNIZERROS_HPP_
#define RECOGNIZERROS_HPP_


#include <ros/ros.h>
#include <ros/package.h>

#include <boost/thread/thread.hpp>

#include <actionlib/server/simple_action_server.h>
#include <bender_speech/DoRecognitionAction.h>
#include <bender_speech/SpeechRecognitionConfig.h>

#include <dynamic_reconfigure/server.h>

#include <sstream>

#include "bender_speech/Recognizer.h"
#include <uchile_util/ParameterServerWrapper.h>

typedef boost::shared_ptr<Recognizer> RecognizerPtr;

class RecognizerROS 
{
public:

    RecognizerROS();
    ~RecognizerROS();
    void executeCB(const bender_speech::DoRecognitionGoalConstPtr &goal);
    void dynamicCallback(bender_speech::SpeechRecognitionConfig &config,uint32_t level);
    void resetRecognizer();
    void updateDirectories(std::string dictionary);
    void recognize(double timeout=15.0);
    void recognizeFile(double timeout, std::string fname);

private:

    ros::NodeHandle nh_;
    ros::Rate loop_rate_;
    AudioSource as_;

    actionlib::SimpleActionServer<bender_speech::DoRecognitionAction> actionServer_;

    bender_speech::DoRecognitionFeedback feedback_;
    bender_speech::DoRecognitionResult result_;

    dynamic_reconfigure::Server<bender_speech::SpeechRecognitionConfig> parameterServer_;
    dynamic_reconfigure::Server<bender_speech::SpeechRecognitionConfig>::CallbackType reconfigureCallback_;


    std::string pkg_dir_;

    std::string hmmdir_;
    std::string modeldir_;
    std::string grammardir_;
    std::string dictdir_;
    std::string threshold_;
    std::string mic_name_;

    double vad_thres_;
    int vad_pre_;
    int vad_post_;
    int vad_start_;
    
    std::string final_result_;
    std::string partial_result_;
    
    RecognizerPtr recognizer_;
    bool in_speech_;
    bool is_on_;
    

};

#endif /* RECOGNIZERROS_HPP_ */