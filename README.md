<!--
 * @Author: Lin Sinan
 * @Github: https://github.com/linsinan1995
 * @Email: mynameisxiaou@gmail.com
 * @LastEditors: Lin Sinan
 * @Description: 
 *               
 *               
 *               
-->
# Pox-Controller

A POX controller strategy to separate the traffic of HAS (HTTP-based adaptive streaming) and FTP to maximize the throughput of HAS traffic under two scenarios: First, HAS is the only traffic in
the network; Second, both HAS and FTP traffic exist in the network. Our solution improves the performance of HAS traffic from the average video
quality from 1.170 to 3.442 with only HAS traffic and from 0.567 to 3.257 with
HAS and FTP sharing the bandwidth. However, since we choose the buffer-
based strategy for HAS, it always starts from low resolution video segments and
takes an amount of time to switch to 4.2MBps coding rate video segments, and
thus the video quality in the first 20 seconds is relatively low.