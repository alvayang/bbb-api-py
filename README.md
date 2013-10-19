bbb-api-py
==========

A very simple python wrapper for bigbluebutton


# Usage

    BBBSALT = '7ae35909bf35d55ccaeeexe058141c8d'
    BBBBASE = u'http://v.1in1.cn/bigbluebutton/api/'
    s = BBB_API(BBBSALT, BBBAPI)
    print s.start_room('测试', 1, '123', '345', 'Welcome', '', 0, 0, 60, '')
    print s.join_room(1, '杨松', 1, '345')

  Read more usage in source code.
