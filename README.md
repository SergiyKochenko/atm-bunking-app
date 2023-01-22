<h1 dir="auto"><a id="user-content-american-pizza---order-system" class="anchor" aria-hidden="true" href="#american-pizza---order-system"><svg class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M7.775 3.275a.75.75 0 001.06 1.06l1.25-1.25a2 2 0 112.83 2.83l-2.5 2.5a2 2 0 01-2.83 0 .75.75 0 00-1.06 1.06 3.5 3.5 0 004.95 0l2.5-2.5a3.5 3.5 0 00-4.95-4.95l-1.25 1.25zm-4.69 9.64a2 2 0 010-2.83l2.5-2.5a2 2 0 012.83 0 .75.75 0 001.06-1.06 3.5 3.5 0 00-4.95 0l-2.5 2.5a3.5 3.5 0 004.95 4.95l1.25-1.25a.75.75 0 00-1.06-1.06l-1.25 1.25a2 2 0 01-2.83 0z"></path></svg></a>ATM Banking Application on Python</h1>
<h2 dir="auto"><a id="user-content-overview" class="anchor" aria-hidden="true" href="#overview"><svg class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M7.775 3.275a.75.75 0 001.06 1.06l1.25-1.25a2 2 0 112.83 2.83l-2.5 2.5a2 2 0 01-2.83 0 .75.75 0 00-1.06 1.06 3.5 3.5 0 004.95 0l2.5-2.5a3.5 3.5 0 00-4.95-4.95l-1.25 1.25zm-4.69 9.64a2 2 0 010-2.83l2.5-2.5a2 2 0 012.83 0 .75.75 0 001.06-1.06 3.5 3.5 0 00-4.95 0l-2.5 2.5a3.5 3.5 0 004.95 4.95l1.25-1.25a.75.75 0 00-1.06-1.06l-1.25 1.25a2 2 0 01-2.83 0z"></path></svg></a>OVERVIEW</h2>
<p dir="auto">I read a lot of articles on GT and Habré about bank cards, ATMs, and so I decided to make my contribution. Below I will try to talk about how the ATM is arranged in terms of software.</p>
<h3>What is an ATM?</h3>
<p>Any ATM is essentially a computer with connected peripherals, an equipment manager and the actual banking application that manages all this economy. All decisions on the issuance of money are made by the server. The ATM only collects information from the client and transmits it to the server.</p>
<h3 dir="auto"><a id="user-content-goals" class="anchor" aria-hidden="true" href="#goals"><svg class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M7.775 3.275a.75.75 0 001.06 1.06l1.25-1.25a2 2 0 112.83 2.83l-2.5 2.5a2 2 0 01-2.83 0 .75.75 0 00-1.06 1.06 3.5 3.5 0 004.95 0l2.5-2.5a3.5 3.5 0 00-4.95-4.95l-1.25 1.25zm-4.69 9.64a2 2 0 010-2.83l2.5-2.5a2 2 0 012.83 0 .75.75 0 001.06-1.06 3.5 3.5 0 00-4.95 0l-2.5 2.5a3.5 3.5 0 004.95 4.95l1.25-1.25a.75.75 0 00-1.06-1.06l-1.25 1.25a2 2 0 01-2.83 0z"></path></svg></a>ATM hardware<br></h3>
<h4>The minimum set of ATM hardware includes:</h4>
<ul dir="auto">
<li>card reader, for reading a customer's card<br></li>
<li>pin pad, for entering a pin code and other information, such as payment / withdrawal amounts<br></li>
<li>function keys on the sides (4 + 4) are an addition connected to the pin-pad. In some modern ATMs, they have been replaced with a touch screen.<br></li>
<li>money dispenser<br></li>
<li>various sensors, backlight<br></li>
</ul>
<h3>Who is running this zoo?</h3>
<p>In order for manufacturers not to suffer with writing drivers that no one needs later, and software developers not to suffer from a variety of solutions for managing a particular piece of hardware, it was decided to unify the whole thing.</p>

<p>This is how the CEN / XFS standard or simply XFS appeared, which stands for eXtension For Financial Services.</p>
<p>The standard describes a client-server architecture consisting of a hardware manager and service providers (read device drivers) that it manages. In the terminology of the standard, a “service provider” is a library that provides a specific set of functions for obtaining information about a device and managing it. Usually this is a dynamic library containing a certain set of standard functions (Open, Close, GetInfo, Execute ) each of which has a number of device-specific arguments.</p>
<p>All interaction with the equipment occurs through the XFS Manager API. For example, the Command parameter of the Execute function might have a value for the bill dispenser:</p>
<p>WFS_CMD_CDM_DISPENSE (a set of money from cassettes)</p>
<p>WFS_CMD_CDM_PRESENT (issuing a pack to a client)</p>
<h3>For card reader:</h3>
<p>WFS_CMD_IDC_RETAIN_CARD (card capture),</p>
<p>WFS_CMD_IDC_READ_TRACK (read tracks)</p>
<p>There are several implementations of XFS managers (including open source ones) written in c ++ and, theoretically, service provider libraries written for one manager should also fit all the others, but in fact sometimes a library written by a specific vendor for a specific XFS manager, works only with this manager.</p>
<p>There is also Java XFS with its own libraries that are not compatible with classic managers.</p>
<h3>Banking application</h3>
<p>The banking app is what you see on the screen when you approach the device. It is designed to collect data from the user, send this data to the host (server) and execute a response from the host. As in the case of hardware (XFS), there are industry protocols (NDC / DDC) by which the application communicates with the host, loads the configuration and interprets it.</p>

<p>Any major ATM manufacturer (Wincor, NCR, Diebold) has its own implementation of both XFS and a banking application.</p>
<p>However, there is alternative software on the market that meets all standards and is not tied to a specific vendor.</p>

<p>I will describe the ATM using the example of NDC as the most common protocol in Europ, but a slightly less popular DDC has a similar principle of operation.</p>

<h3>How does it work</h3>

<p>At any given time, the ATM is in one of the following operating modes:</p>

<ul dir="auto">
<li>Power Up- Loading<br></li>
<li>Offline - No connection to the server, connect<br></li>
<li>Supervisor - a collector or service engineer works<br></li>
<li>Out of service - the ATM does not work because it is out of order, the money has run out, or simply someone at the bank has switched it to this mode.<br></li>
<li>In service is the main mode of operation, familiar to all those who have bank cards.<br></li>
</ul>

<p>In the In service mode, the ATM is in one of the states (state), with a number from 001 to 999, and a 25-character description string.</p>

<p>The first character of this line is the type of the state (denoted by the letters A..Z and also a..z and some characters (,'.?)), it defines the collection. The remaining 24 characters are 8 decimal 3-digit numbers, each of which is a specific state setting (screen number to display, conditions for switching to the state, list of actions). There can be any number of states of the same type.</p>
<h3>In service mode</h3>
<p>When the service mode starts, the ATM automatically starts executing state 000. This is usually state A (Card read state). In this state, the ATM displays a screen prompting you to insert a card and puts the card reader into the receiving mode. The state is also responsible for reading the map and branching depending on the results of this operation.</p>
<p>Below is an example configuration of a typical state A:
000 A001001011008004002001104</p>
<ul dir="auto">
<li>000 - state number<br></li>
<li>A - state type (Card read state)<br></li>
<li>001 - Screen number<br></li>
<li>001 - state number to go to in case of successful card reading<br></li>
<li>011 - state number to go to in case of map reading errors<br></li>
  <li>008 - read condition 1<br></li>
  <li>004 - read condition 2<br></li>
  <li>002 - read condition 3<br></li>
  <li>001 - card return condition (immediately after reading or upon completion of the operation)<br></li>
  <li>104 - transition state if the card is unknown to the bank<br></li>
</ul>
<p>Let's go through the parameters in more detail:</p>
<p>State type - everything is clear here: having determined the type of the state, the application knows how to interpret further parameters.
Screen number - is a link to a string with a text description of the screen that is displayed during the operation of this state.</p>

<p>Not every state has a screen.</p>

<p>A screen can be numbered from 000 to 999. Screens that differ by 100 are usually reserved for different languages. Thus screen 010 and screen 210 are most likely multilingual versions of the same screen. I'll talk about screens a little later.</p>

<p>Transition state number in case of successful reading of the card - what state the application will start to execute if the card is recognized and the data is read successfully.</p>

<p>In addition to states and screens, the ATM has another important configuration parameter - the financial institution table. The table of financial institutions contains data on which cards belong to which bank, how to correctly parse the data read from the card tracks, and what to do next depending on this data. For example, if the card is local, then you can execute one script, if the card is a third-party bank, then you need to disable the script branch with mobile payments and checking the balance.</p>

<p>The number of the transition state in case of problems with reading the card - if the card could not be read according to any of the proposed conditions - go to the state specified in this parameter. As a rule, this is the state J (Close state) on which we give the card, show a screen with an offer to pick it up and activate the timer after which the card retention mechanism will be launched. State J is also the last state in case of a successful transaction.</p>

<p>Conditions for reading the card (3 parameters in a row) are bit masks that indicate the track numbers that need to be read, and interaction with the chip, if any.</p>

<p>For example, Read Chip, Read Track 2 and Track 1, Read Track 1. If at least one of the conditions is met, then the other conditions are not met and the card is considered read. If none of the conditions is met, the card is considered unread.</p>

<p>Card return condition - the ATM can return the cards immediately after reading, or it can do it at the end after all operations are completed.</p>

<p>The rest of the states are arranged in a similar way:</p>

<ul dir="auto">
<li>There are states for reading the sum from the keyboard and placing it in a special internal buffer;<br></li>
<li>There are states for reading a pin code with a pin pad and then receiving a pin block into a special buffer;<br></li>
<li>There are states for checking the entered data (for example, if the entered amount is less than the minimum amount, then there is a redirect to the state with an error message);<br></li>
<li>There are states for selecting using the side keys (so-called FDK) and placing the characters of these keys (ABCD FGHI) in a special 8-byte buffer;<br></li>
<li>There are states for resetting and presetting buffers.<br></li>
</ul>

<p>Going through all these states, the application sooner or later reaches the state of interaction with the host - state I (Transaction Request State). On this state, a request is formed from the data collected on previous states and sent to the server. The request is an ATM ID (Logical Unit Number), data from the card tracks, data on previous transactions, data from the amount buffers, pin block, and function key presses (FDK buffer). The data is separated by a delimiter character. The server application receives the request and analyzes the FDK buffer - it is from the contents of this buffer that the host understands what the ATM wants. Then, depending on the decision made, sends a response containing:</p>

<ul dir="auto">
<li>ID of the action to be performed;<br></li>
<li>screen number to be shown during this action;<br></li>
<li>the contents of the check, if the check needs to be printed;<br></li>
<li>The state to go to when the action completes.<br></li>
</ul>


<p>In a special buffer, the number of banknotes to be dispensed from each cassette is transmitted (if this is a cash withdrawal operation). It is the number of banknotes, because the ATM does not know the denominations of the issued money for it, these are just pieces of paper in cassettes.</p>

<p>Upon completion of the required actions, the application sends a confirmation to the host and goes to the specified state. As a rule, this is the J state already known to us. In case of any failure, the application sends a failure message to the host and waits for a new Transaction Reply with a transition to a new state.</p>
<h3>Now about screens</h3>

<p>The ATM screen is a field of 32x16 cells. The screen can contain both graphic information and textual information, which is positioned relative to the cells. Fonts can be double height.</p>

<p>The screen description is a line of text interspersed with control characters such as screen clearing, cursor position, font size. In most modern banks today, text is used only when entering amounts, and in other cases, the screen is just a single picture. However, there are also completely text screens.</p>

<p>An example of a screen displaying a picture from a table of pictures (\0c\1bP2018\1b\5c)</p>

<p>It is to such screens that the state parameters refer.</p>

<p>The set of states, screens, FITs, timers is called an ATM scenario. Each scenario has its own number. After loading the ATM and connecting it to the network, it sends a message to the host in which it reports its ID and configuration number. If the configuration needs to be updated, the host switches the ATM to the “Out Of Service” mode and starts loading the necessary parameters of the new configuration. The last parameter is the configuration number. In a similar way, the keys for encrypting the pin block, for popping, and master keys are loaded.</p>

<p>Here, in a nutshell, is how an ATM works. I hope this information is useful to someone.</p>