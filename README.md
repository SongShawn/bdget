
2018-01-11:
当前的实现太简单了，直接使用urllib2库中的urlopen打开一个url，这是一个同步接口，大量的时间浪费在等待网络I/O响应上，
经过实际测试，没解析100个url，需要1分钟，这太慢了，我们有太多的url需要解析，等不起呀。

而解决这个问题最直接的办法就是引入异步网络I/O的模型。
1. 不再使用urllib2模块，直接使用socket、select模块来搞定异步，再引入多线程。
2. 使用成熟的异步网络I/O模块。（Twisted、Concurrence）


第一个版本先使用Twisted吧，不过貌似很复杂的一个模块。