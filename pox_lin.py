# -*- coding: utf-8 -*-
# @Author: Lin Sinan
# @Date:   2020-05-27 15:55:28
# @Last Modified by:   lnan951
# @Last Modified time: 2020-06-01 23:44:15

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpid_to_str
from pox.lib.packet import ethernet,ipv4,tcp
from pox.lib.addresses import IPAddr, EthAddr
#!/usr/bin/python
# Copyright 2012 James McCauley
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This component is for use with the OpenFlow tutorial.

It acts as a simple hub, but can be modified to act like an L2
learning switch.

It's roughly similar to the one Brandon Heller did for NOX.
"""

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpid_to_str
from pox.lib.packet import ethernet,ipv4,tcp
from pox.lib.addresses import IPAddr, EthAddr

log = core.getLogger()
clientIP_str = "172.16.0.1"
serverIP_str = "172.16.1.1"
#clientIP_str = "10.0.1.1"
#serverIP_str = "10.0.2.1"

class Pox_seperate_http_ftp (object):
  """
  A Tutorial object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)

    # Use this table to keep track of which ethernet address is on
    # which switch port (keys are MACs, values are ports).
    self.mac_to_port = {}


  def resend_packet (self, packet_in, out_port):
    """
    instructs the switch to resend a packet that it had sent to us.
    "packet_in" is the ofp_packet_in object the switch had sent to the
    controller due to a table-miss.
    """
    msg = of.ofp_packet_out()
    msg.data = packet_in

    # Add an action to send to the specified port
    action = of.ofp_action_output(port = out_port)
    msg.actions.append(action)

    # Send message to switch
    self.connection.send(msg)

  def act_like_routers_in_legacy_case (self, packet, packet_in):
    log.debug("Packet captured by first time by switch %s at input port %d" % (dpid_to_str(self.connection.dpid), packet_in.in_port))


    # if it is a http packet
    #if captured at s1
    if dpid_to_str(self.connection.dpid) == "00-00-00-00-00-01":
      self.strategy_s1(packet, packet_in)
    #if captured at s2
    if dpid_to_str(self.connection.dpid) == "00-00-00-00-00-02":
      self.strategy_s2(packet, packet_in)
    #if captured at s3
    if dpid_to_str(self.connection.dpid) == "00-00-00-00-00-03" :
      self.strategy_s3(packet, packet_in)


  def strategy_s1(self, packet, packet_in):
    if packet_in.in_port == 3:
      isHttp, is_dst = self.http_packet(packet)
      if isHttp:
        log.debug("We send out directly packet to s3 via port 2(s3-s2)")
        self.resend_packet(packet_in, 2)
        log.debug("Installing flow ...")
        msg = of.ofp_flow_mod()
        msg.priority = 35555
        msg.match.nw_proto = 6 # tcp
        if is_dst:
          msg.match.tp_dst = 80
        else:
          msg.match.tp_src = 80
        msg.match.dl_type = packet.type
        msg.match.in_port = packet_in.in_port
        msg.actions.append(of.ofp_action_output(port=2))
        self.connection.send(msg)
      else:
        log.debug("We send out directly packet to s3 via port 1")
        self.resend_packet(packet_in, 1)
        log.debug("Installing flow ...")
        msg = of.ofp_flow_mod()
        msg.match.dl_type = packet.type
        msg.match.in_port = packet_in.in_port
        msg.actions.append(of.ofp_action_output(port=1))
        self.connection.send(msg)

    elif packet_in.in_port == 1 :
        log.debug("We send out directly packet to h1 via port 3")
        self.resend_packet(packet_in, 3)
        log.debug("Installing flow ...")
        msg = of.ofp_flow_mod()
        msg.match.dl_type = packet.type
        msg.match.in_port = packet_in.in_port
        msg.actions.append(of.ofp_action_output(port=3))
        self.connection.send(msg)

    elif packet_in.in_port == 2:
        log.debug("We send out directly packet to h1 via port 3")
        self.resend_packet(packet_in, 3)
        log.debug("Installing flow ...")
        msg = of.ofp_flow_mod()
        msg.match.dl_type = packet.type
        msg.match.in_port = packet_in.in_port
        msg.actions.append(of.ofp_action_output(port=3))
        self.connection.send(msg)

  def strategy_s2(self, packet, packet_in):
    if packet_in.in_port == 1 :
        log.debug("We send out directly packet to s3 via port 2")
        self.resend_packet(packet_in, 2)
        log.debug("Installing flow ...")
        msg = of.ofp_flow_mod()
        msg.match.dl_type = packet.type
        msg.match.in_port = packet_in.in_port
        msg.actions.append(of.ofp_action_output(port=2))
        self.connection.send(msg)
    elif packet_in.in_port == 2:
        log.debug("We send out directly packet to s1 via port 1")
        self.resend_packet(packet_in, 1)
        log.debug("Installing flow ...")
        msg = of.ofp_flow_mod()
        msg.match.dl_type = packet.type
        msg.match.in_port = packet_in.in_port
        msg.actions.append(of.ofp_action_output(port=1))
        self.connection.send(msg)

  def strategy_s3(self, packet, packet_in):
    isHttp, is_dst = self.http_packet(packet)
    if packet_in.in_port == 3:
      if isHttp:
        log.debug("We send out directly packet to s1 via port 1")
        self.resend_packet(packet_in, 2)
        log.debug("Installing flow ...")
        msg = of.ofp_flow_mod()
        msg.priority = 35555
        msg.match.nw_proto = 6 # tcp
        if is_dst:
          msg.match.tp_dst = 80
        else:
          msg.match.tp_src = 80
        msg.match.dl_type = packet.type
        msg.match.in_port = packet_in.in_port
        msg.actions.append(of.ofp_action_output(port=2))
        self.connection.send(msg)
      else:
        log.debug("We send out directly packet to s1 via port 1")
        self.resend_packet(packet_in, 1)
        log.debug("Installing flow ...")
        msg = of.ofp_flow_mod()
        msg.match.dl_type = packet.type
        msg.match.in_port = packet_in.in_port
        msg.actions.append(of.ofp_action_output(port=1))
        self.connection.send(msg)

    elif packet_in.in_port == 1 :
      log.debug("We send out directly packet to h2 via port 3")
      self.resend_packet(packet_in, 3)
      log.debug("Installing flow ...")
      msg = of.ofp_flow_mod()
      msg.match.dl_type = packet.type
      msg.match.in_port = packet_in.in_port
      msg.actions.append(of.ofp_action_output(port=3))
      self.connection.send(msg)

    elif packet_in.in_port == 2 :
      log.debug("We send out directly packet to h2 via port 3")
      self.resend_packet(packet_in, 3)
      log.debug("Installing flow ...")
      msg = of.ofp_flow_mod()
      msg.match.dl_type = packet.type
      msg.match.in_port = packet_in.in_port
      msg.actions.append(of.ofp_action_output(port=3))
      self.connection.send(msg)

  def http_packet(self, packet): # to identify a HTTP packet
    http_pkt = 0
    is_dst = False
    foundtcp = packet.find("tcp")
    if foundtcp:
      print foundtcp.dstport, " ", foundtcp.srcport
    if packet.type == ethernet.IP_TYPE:
      ipv4_packet = packet.find("ipv4")
      if ipv4_packet.protocol == ipv4.TCP_PROTOCOL:
        tcp_segment = ipv4_packet.find("tcp")
        if tcp_segment.dstport == 80:
          http_pkt = 1
          is_dst = True
        if tcp_segment.srcport == 80:
          http_pkt = 1
          is_dst = False
    return http_pkt, is_dst

  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """

    packet = event.parsed
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    # Comment out the following line and uncomment the one after
    # when starting the exercise.
    #self.act_like_hub(packet, packet_in)
    # self.act_like_switch(packet, packet_in)
    self.act_like_routers_in_legacy_case(packet, packet_in)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Pox_seperate_http_ftp(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
