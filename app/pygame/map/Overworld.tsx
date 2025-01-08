<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.10" tiledversion="1.11.0" name="Overworld" tilewidth="16" tileheight="16" tilecount="1440" columns="40">
 <image source="tileset/Overworld.png" width="640" height="576"/>
 <tile id="0" type="grass"/>
 <tile id="16" type="water"/>
 <tile id="17" type="water"/>
 <tile id="18" type="water"/>
 <tile id="19" type="water"/>
 <tile id="20" type="water"/>
 <tile id="21" type="water"/>
 <tile id="40" type="water"/>
 <tile id="41" type="water"/>
 <tile id="42" type="water"/>
 <tile id="43" type="water"/>
 <tile id="46">
  <properties>
   <property name="can_reach" type="bool" value="false"/>
  </properties>
 </tile>
 <tile id="47">
  <properties>
   <property name="can_reach" type="bool" value="false"/>
  </properties>
 </tile>
 <tile id="48">
  <properties>
   <property name="can_reach" type="bool" value="false"/>
  </properties>
 </tile>
 <tile id="49">
  <properties>
   <property name="can_reach" type="bool" value="false"/>
  </properties>
 </tile>
 <tile id="50">
  <properties>
   <property name="can_reach" type="bool" value="false"/>
  </properties>
 </tile>
 <tile id="56" type="water"/>
 <tile id="57" type="water"/>
 <tile id="58" type="water"/>
 <tile id="59" type="water"/>
 <tile id="60" type="water"/>
 <tile id="61" type="water"/>
 <tile id="80" type="water"/>
 <tile id="81" type="water"/>
 <tile id="82" type="water"/>
 <tile id="83" type="water"/>
 <tile id="86">
  <properties>
   <property name="can_reach" type="bool" value="false"/>
  </properties>
 </tile>
 <tile id="87">
  <properties>
   <property name="can_reach" type="bool" value="false"/>
  </properties>
 </tile>
 <tile id="88">
  <properties>
   <property name="can_reach" type="bool" value="false"/>
  </properties>
 </tile>
 <tile id="89">
  <properties>
   <property name="can_reach" type="bool" value="false"/>
  </properties>
 </tile>
 <tile id="90">
  <properties>
   <property name="can_reach" type="bool" value="false"/>
  </properties>
 </tile>
 <tile id="96" type="water"/>
 <tile id="97" type="water"/>
 <tile id="98" type="water"/>
 <tile id="99" type="water"/>
 <tile id="100" type="water"/>
 <tile id="101" type="water"/>
 <tile id="120" type="grass"/>
 <tile id="121" type="grass"/>
 <tile id="122" type="grass"/>
 <tile id="123" type="water"/>
 <tile id="124" type="water"/>
 <tile id="125" type="water"/>
 <tile id="126">
  <properties>
   <property name="can_reach" type="bool" value="false"/>
  </properties>
 </tile>
 <tile id="127">
  <properties>
   <property name="can_reach" type="bool" value="false"/>
  </properties>
 </tile>
 <tile id="128">
  <properties>
   <property name="can_reach" type="bool" value="false"/>
  </properties>
 </tile>
 <tile id="129">
  <properties>
   <property name="can_reach" type="bool" value="false"/>
  </properties>
 </tile>
 <tile id="130">
  <properties>
   <property name="can_reach" type="bool" value="false"/>
  </properties>
 </tile>
 <tile id="136" type="water"/>
 <tile id="137" type="water"/>
 <tile id="138" type="water"/>
 <tile id="139" type="water"/>
 <tile id="140" type="water"/>
 <tile id="141" type="water"/>
 <tile id="160" type="grass"/>
 <tile id="162" type="grass"/>
 <tile id="163" type="water">
  <objectgroup draworder="index" id="2">
   <object id="1" x="6.99051" y="8.08185" width="2.15319" height="1.20933"/>
   <object id="2" x="6.04664" y="-1.15034"/>
  </objectgroup>
 </tile>
 <tile id="164" type="water"/>
 <tile id="165" type="water"/>
 <tile id="166">
  <properties>
   <property name="can_reach" type="bool" value="false"/>
  </properties>
 </tile>
 <tile id="167">
  <properties>
   <property name="can_reach" type="bool" value="false"/>
  </properties>
 </tile>
 <tile id="168">
  <properties>
   <property name="can_reach" type="bool" value="true"/>
  </properties>
 </tile>
 <tile id="169">
  <properties>
   <property name="can_reach" type="bool" value="false"/>
  </properties>
 </tile>
 <tile id="170">
  <properties>
   <property name="can_reach" type="bool" value="false"/>
  </properties>
 </tile>
 <tile id="200" type="grass"/>
 <tile id="201" type="grass"/>
 <tile id="202" type="grass"/>
 <tile id="242" type="grass"/>
 <tile id="243" type="grass">
  <properties>
   <property name="has_border" type="bool" value="true"/>
  </properties>
  <objectgroup draworder="index" id="2">
   <object id="2" template="bottom_border_collision.tx" x="0" y="12"/>
  </objectgroup>
 </tile>
 <tile id="244" type="grass">
  <objectgroup draworder="index" id="2">
   <object id="1" x="1.61439e-06" y="9.0356" width="5.12098" height="6.94284"/>
  </objectgroup>
 </tile>
 <tile id="258" type="water">
  <properties>
   <property name="Animated" type="bool" value="true"/>
  </properties>
  <animation>
   <frame tileid="258" duration="100"/>
   <frame tileid="259" duration="100"/>
   <frame tileid="260" duration="100"/>
  </animation>
 </tile>
 <tile id="259" type="water"/>
 <tile id="260" type="water"/>
 <tile id="282" type="grass">
  <properties>
   <property name="has_border" type="bool" value="true"/>
  </properties>
  <objectgroup draworder="index" id="2">
   <object id="1" template="right_border_collision.tx" x="12" y="0"/>
  </objectgroup>
 </tile>
 <tile id="283" type="water">
  <objectgroup draworder="index" id="2">
   <object id="2" x="6.40665e-06" y="1.39104e-06" width="16.0523" height="15.9538"/>
  </objectgroup>
 </tile>
 <tile id="284" type="grass">
  <properties>
   <property name="has_border" type="bool" value="true"/>
  </properties>
  <objectgroup draworder="index" id="2">
   <object id="3" template="left_border_collision.tx" name="left_border" x="0" y="0" visible="1"/>
  </objectgroup>
 </tile>
 <tile id="298" type="water">
  <properties>
   <property name="Animated" type="bool" value="true"/>
  </properties>
  <animation>
   <frame tileid="298" duration="100"/>
   <frame tileid="299" duration="100"/>
   <frame tileid="300" duration="100"/>
  </animation>
 </tile>
 <tile id="299" type="water"/>
 <tile id="300" type="water"/>
 <tile id="322" type="grass">
  <objectgroup draworder="index" id="2">
   <object id="1" x="10.9067" y="1.61833e-05" width="5.12098" height="4.97323"/>
  </objectgroup>
 </tile>
 <tile id="323" type="grass">
  <properties>
   <property name="has_border" type="bool" value="true"/>
  </properties>
  <objectgroup draworder="index" id="2">
   <object id="2" template="top_border_collision.tx" x="0" y="0"/>
  </objectgroup>
 </tile>
 <tile id="324" type="grass">
  <objectgroup draworder="index" id="2">
   <object id="1" x="1.61439e-06" y="0.0246359" width="5.12098" height="4.97323"/>
  </objectgroup>
 </tile>
 <tile id="338" type="water">
  <properties>
   <property name="Animated" type="bool" value="true"/>
  </properties>
  <animation>
   <frame tileid="338" duration="100"/>
   <frame tileid="339" duration="100"/>
   <frame tileid="340" duration="100"/>
  </animation>
 </tile>
 <tile id="339" type="water"/>
 <tile id="340" type="water"/>
 <tile id="360" type="grass"/>
 <tile id="361" type="grass"/>
 <tile id="362">
  <properties>
   <property name="border" value="left,up"/>
  </properties>
  <objectgroup draworder="index" id="2">
   <object id="2" template="top_border_collision.tx" x="0" y="0"/>
   <object id="5" template="left_border_collision.tx" name="left_border" x="0" y="0" visible="1"/>
  </objectgroup>
 </tile>
 <tile id="363">
  <properties>
   <property name="border" value="right,up"/>
  </properties>
  <objectgroup draworder="index" id="2">
   <object id="1" template="top_border_collision.tx" x="0" y="0"/>
   <object id="2" template="right_border_collision.tx" x="12" y="0"/>
  </objectgroup>
 </tile>
 <tile id="364" type="grass">
  <properties>
   <property name="border" value="left"/>
  </properties>
  <objectgroup draworder="index" id="2">
   <object id="1" template="left_border_collision.tx" name="left_border" x="0" y="0" visible="1"/>
  </objectgroup>
 </tile>
 <tile id="365" type="grass"/>
 <tile id="366" type="grass">
  <properties>
   <property name="border" value="right"/>
  </properties>
  <objectgroup draworder="index" id="2">
   <object id="1" template="right_border_collision.tx" x="12" y="0"/>
  </objectgroup>
 </tile>
 <tile id="367" type="grass"/>
 <tile id="368" type="grass"/>
 <tile id="377" type="water">
  <properties>
   <property name="Animated" type="bool" value="true"/>
  </properties>
  <animation>
   <frame tileid="377" duration="100"/>
   <frame tileid="417" duration="100"/>
   <frame tileid="458" duration="100"/>
  </animation>
 </tile>
 <tile id="378" type="water">
  <properties>
   <property name="Animated" type="bool" value="true"/>
  </properties>
  <animation>
   <frame tileid="378" duration="100"/>
   <frame tileid="418" duration="100"/>
   <frame tileid="459" duration="100"/>
  </animation>
 </tile>
 <tile id="379" type="water">
  <properties>
   <property name="Animated" type="bool" value="true"/>
  </properties>
  <animation>
   <frame tileid="379" duration="100"/>
   <frame tileid="419" duration="100"/>
   <frame tileid="460" duration="100"/>
  </animation>
 </tile>
 <tile id="400" type="grass"/>
 <tile id="401" type="grass"/>
 <tile id="402">
  <properties>
   <property name="border" value="left,down"/>
  </properties>
  <objectgroup draworder="index" id="2">
   <object id="3" template="left_border_collision.tx" name="left_border" x="0" y="0" visible="1"/>
   <object id="4" template="bottom_border_collision.tx" x="0" y="12"/>
  </objectgroup>
 </tile>
 <tile id="403">
  <properties>
   <property name="border" value="right,down"/>
  </properties>
  <objectgroup draworder="index" id="2">
   <object id="3" template="bottom_border_collision.tx" x="0" y="12"/>
   <object id="4" template="right_border_collision.tx" x="12" y="0"/>
  </objectgroup>
 </tile>
 <tile id="404" type="grass">
  <properties>
   <property name="border" value="left"/>
  </properties>
  <objectgroup draworder="index" id="2">
   <object id="1" template="left_border_collision.tx" name="left_border" x="0" y="0" visible="1"/>
  </objectgroup>
 </tile>
 <tile id="405" type="grass"/>
 <tile id="406" type="grass">
  <properties>
   <property name="border" value="right"/>
  </properties>
  <objectgroup draworder="index" id="2">
   <object id="1" template="right_border_collision.tx" x="12" y="0"/>
  </objectgroup>
 </tile>
 <tile id="407" type="grass"/>
 <tile id="408" type="grass"/>
 <tile id="417" type="water"/>
 <tile id="418" type="water"/>
 <tile id="419" type="water"/>
 <tile id="444" type="grass">
  <properties>
   <property name="border" value="left,down"/>
  </properties>
  <objectgroup draworder="index" id="2">
   <object id="1" template="bottom_border_collision.tx" x="0" y="12"/>
   <object id="2" template="left_border_collision.tx" name="left_border" x="0" y="0" visible="1"/>
  </objectgroup>
 </tile>
 <tile id="445" type="grass">
  <properties>
   <property name="border" value="down"/>
  </properties>
  <objectgroup draworder="index" id="2">
   <object id="1" template="bottom_border_collision.tx" x="0" y="12"/>
  </objectgroup>
 </tile>
 <tile id="446" type="grass">
  <properties>
   <property name="border" value="right,down"/>
  </properties>
  <objectgroup draworder="index" id="2">
   <object id="1" template="right_border_collision.tx" x="12" y="0"/>
   <object id="2" template="bottom_border_collision.tx" x="0" y="12"/>
  </objectgroup>
 </tile>
 <tile id="447" type="rock"/>
 <tile id="448" type="rock"/>
 <tile id="458" type="water"/>
 <tile id="459" type="water"/>
 <tile id="460" type="water"/>
 <tile id="484" type="rock"/>
 <tile id="485" type="rock"/>
 <tile id="486" type="rock"/>
 <tile id="524" type="rock"/>
 <tile id="525" type="rock"/>
 <tile id="526" type="rock"/>
 <tile id="564" type="rock"/>
 <tile id="565" type="rock"/>
 <tile id="566" type="rock"/>
 <tile id="608" type="rock"/>
 <tile id="609" type="rock"/>
 <tile id="611" type="rock"/>
 <tile id="612" type="rock"/>
 <tile id="651" type="rock"/>
 <tile id="652" type="rock"/>
 <tile id="689">
  <properties>
   <property name="border" value="right,down"/>
  </properties>
  <objectgroup draworder="index" id="2">
   <object id="1" template="right_border_collision.tx" x="12" y="0"/>
   <object id="2" template="bottom_border_collision.tx" x="0" y="12"/>
  </objectgroup>
 </tile>
 <tile id="690">
  <properties>
   <property name="border" value="left,down"/>
  </properties>
  <objectgroup draworder="index" id="2">
   <object id="1" template="left_border_collision.tx" name="left_border" x="0" y="0" visible="1"/>
   <object id="2" template="bottom_border_collision.tx" x="0" y="12"/>
  </objectgroup>
 </tile>
 <tile id="728" type="rock"/>
 <tile id="729" type="rock"/>
 <tile id="730" type="rock"/>
 <tile id="766" type="rock"/>
 <tile id="767" type="rock"/>
 <tile id="768" type="rock"/>
 <tile id="769" type="rock"/>
 <tile id="770" type="rock"/>
 <tile id="800" type="rock"/>
 <tile id="801" type="rock"/>
 <tile id="802" type="rock"/>
 <tile id="803" type="rock"/>
 <tile id="804" type="rock"/>
 <tile id="805" type="rock"/>
 <tile id="806" type="rock"/>
 <tile id="807" type="rock"/>
 <tile id="809" type="rock"/>
 <tile id="810" type="rock"/>
 <tile id="844" type="rock"/>
 <tile id="845" type="rock"/>
 <tile id="846" type="rock"/>
 <tile id="847" type="rock"/>
 <wangsets>
  <wangset name="Unnamed Set" type="corner" tile="-1">
   <wangcolor name="Water-edge" color="#ff0000" tile="-1" probability="1"/>
   <wangtile tileid="242" wangid="0,0,0,1,0,0,0,0"/>
   <wangtile tileid="243" wangid="0,0,0,1,0,1,0,0"/>
   <wangtile tileid="244" wangid="0,0,0,0,0,1,0,0"/>
   <wangtile tileid="282" wangid="0,1,0,1,0,0,0,0"/>
   <wangtile tileid="283" wangid="0,1,0,1,0,1,0,1"/>
   <wangtile tileid="284" wangid="0,0,0,0,0,1,0,1"/>
   <wangtile tileid="322" wangid="0,1,0,0,0,0,0,0"/>
   <wangtile tileid="323" wangid="0,1,0,0,0,0,0,1"/>
   <wangtile tileid="324" wangid="0,0,0,0,0,0,0,1"/>
   <wangtile tileid="362" wangid="0,1,0,0,0,1,0,1"/>
   <wangtile tileid="363" wangid="0,1,0,1,0,0,0,1"/>
   <wangtile tileid="402" wangid="0,0,0,1,0,1,0,1"/>
   <wangtile tileid="403" wangid="0,1,0,1,0,1,0,0"/>
  </wangset>
 </wangsets>
</tileset>
