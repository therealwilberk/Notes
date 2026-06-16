# Why Robots Still Can’t Do Science

**Source:** Nautilus  
**Author:** Grigori Guitchounts  
**Date:** 2026-06-12  
**Link:** https://nautil.us/why-robots-still-cant-do-science-1281910/

---

**The Physicality of Science**

If a neuroscientist wants to understand how neurons in a mouse brain represent its bodily processes—satiety, temperature, heart rate—they implant tiny lenses to peer deep into the brain. Grace Chahyadinata, a third-year graduate student in a neuroscience lab at Harvard, has performed this surgery hundreds of times. When I asked her what makes a good brain surgery, she paused, then laughed. “It’s more of an art than a science,” she said. “You go based on vibes.”

The procedure begins with anesthesia, followed by the delicate work of fitting a mouse’s head into a stereotaxic frame. Two metal bars grip the skull at the interaural ridges, while the animal’s incisors hook over a bite bar at the front. The geometry matters: a few millimeters off, and you’ve killed the experiment. First-year students learning this technique often stumble here, fumbling a limp, anesthetized mouse into position without hurting it. This physical comedy continues until the initial dose of anesthetic wears off, at which point the student must carry the mouse back to the induction chamber to put it under again. The process repeats. Thirty minutes can pass before the mouse’s head sits in the frame, and the experiment hasn’t even started.

“A lot of these things aren’t teachable,” Chahyadinata told me. “Of course there’s the bregma”—the point on the skull where two sutures meet, used as a landmark—“but everyone’s bregma is different.” She had recently been training an undergraduate, and the task of explaining what she knew kept tripping her up. “People can’t really tell you what the secret recipe is to good targeting. Sometimes you just see it and you think, you should go more lateral or more medial.”

Most neuroscientists know this ritual—the setup has barely changed since the 1950s. Science runs on manual labor. Graduate students hone their craft over years, practicing esoteric procedures like a pianist running scales. Some love this physical work. Others are stunned to discover that asking interesting questions requires so much unglamorous repetition.

Science is sometimes drawn as a cycle: observe, hypothesize, experiment, analyze, repeat. AI is turning the early steps topsy-turvy. AlphaFold predicts the shape of any protein. LLMs read the whole literature in an afternoon. New foundation models conjure molecules a chemist never would.

AI is now crossing into robotics, and the prospect of robots in the lab is no longer hypothetical. But can machines learn to do what Chahyadinata does with her hands? (Whether they should is another question.)

**Medra AI Aims to Bring Adaptive Robots Into the Lab**

The dream of automating the laboratory is not new. In 1957, a clinical chemist named Leonard Skeggs brought to market the AutoAnalyzer, a machine that ran blood samples through a flowing stream broken up by air bubbles. A single technician could now run 60 tests an hour. Two decades later, the Zymark Corporation introduced the Zymate, a reprogrammable two-foot arm that could pipette, pour, and press buttons. By the 1990s, pharmaceutical companies were screening hundreds of thousands of compounds a day. Each generation chased the same goal: more, faster.

But the underlying philosophy never changed: Automation borrowed its logic from the assembly line. Machines repeated fixed sequences in tightly controlled environments, but when reality pushed back—a cap stuck, a tube misplaced, a reagent behaving oddly—the system broke down. The adaptive, irregular work of research science remained stubbornly manual. Now, a wave of well-funded startups is trying to change that. One is Medra AI.

Michelle Lee, the CEO and founder of Medra AI, is certain robots belong in the lab. Where the self-driving labs of the past decades automate fixed protocols, her Bay Area startup wants to build robots that can adapt, working flexibly in the mess of a real lab bench.

But robots in the real world are famously brittle. Blooper reels online show them falling over, misjudging distances, failing to coordinate what they see with how they move. Even when they succeed, the results can feel faintly absurd. One clip shows a humanoid robot placing blue balls into a Ziplock bag, moving so slowly it seems submerged in molasses, its cameras leaning in as if in deep concentration. The caption reads: “pov you took a 1000 mg edible before going to your job as a Trader Joe’s cashier.”

![](https://lede-admin.nautil.us/wp-content/uploads/sites/70/2026/06/pq-01_a2c2ab.png?w=710)

Lee earned her Ph.D. at Stanford, fusing sensory data for robotic perception and control. Late in her Ph.D., she started visiting biology labs. The automation she saw, even in cutting-edge facilities, was antiquated. “I was pretty underwhelmed,” she said. “The technology they were showing me was from 10, even 20 years ago.”

Lee puts the indictment more bluntly. “Software-based automation is extremely limited, especially when you’re talking about manipulating physical objects,” she said. “This is industrial automation from the last 40 years: You program robots to do exactly what you tell them to do. If there’s any deviation in the physical world—which happens all the time—you’re going to mess up.”

That approach works well in manufacturing, where the environment can be tightly controlled. “If you build all the tools in place, you can have a very successful manufacturing line,” Lee said. “But a lab is not a manufacturing line.”

Medra’s bet diverges from self-driving labs in one direction and from most other AI-for-science work in another. The cognitive efforts—literature-mining agents, autonomous hypothesis generators—focus on reasoning and planning. Lee’s argument is that you can think about science till the soup gets cold, but eventually you have to do the experiments. “For us, we talk about physical AI scientists,” she said. “You need physical AI first to actually do science.”

Lee’s bet is that the way to scale isn’t to redesign every scientific instrument, but to build robots that can use the ones we already have—pipettes, centrifuges, PCR machines, Falcon tubes, tools designed for humans. When I first heard this, it struck me as counterintuitive. Why build robots that press buttons or twist caps instead of creating fully automated instruments?

It’s simple mathematics, as Mos Def might say. There are an estimated eight to 10,000 distinct scientific instruments in use today, and only a few hundred have been automated, mostly through software. “An automated centrifuge isn’t that different from a normal centrifuge,” Lee said. “It’s really just software. But it costs $80,000. A normal centrifuge costs $2,000.”

For instrument manufacturers like Thermo Fisher, the market for fully automated devices is too small to justify large production runs. Medra’s bet is that instead of building expensive specialized instruments, you can build one general-purpose robot that uses the cheap ones. Where traditional automation scaled throughput, Lee is scaling capability.

Medra isn’t building its own robots. “We’re using general-purpose robots,” Lee told me. “These are the same robots used on Toyota manufacturing lines.” If her approach works, the lab of the future won’t be a Strateos or an Emerald Cloud Lab—remote, automated facilities designed to keep humans out. Lee doesn’t want humans out of the lab; she wants them training robots in it. “We want it to feel like you’re working with the best research assistant possible,” she said. “On the science side, that’s where superintelligence is exciting—proposing hypotheses, talking ideas at the high level. But on the physically doing the science, you have to think of it as training an RA.”

![](https://lede-admin.nautil.us/wp-content/uploads/sites/70/2026/06/pq-02_3242fa.png?w=710)

What Lee described would be familiar to anyone who has mentored a new lab member. “You have all the nuances in science—you need to bend the pipette just like this, you need to have the tip touch the wall first, you need to stir in this particular way,” she said. “We want to make it as simple as teaching an RA where you’re watching it and say: ‘Wait, stop. Try that again. No, that’s not how I want you to do it. I want you to go deeper.’”

I pictured a robot lifting an anesthetized mouse, fixing its head into a stereotaxic frame, hooking its incisors onto the bite bar, and beginning surgery. The picture was hard to believe. So much of what a scientist does isn’t just manual labor—it’s labor that requires real dexterity and constant tacit judgement.

Lee knows what’s standing in the way. “Three years from now, Medra will be switching to humanoids,” she told me. “The hardware isn’t good enough yet, but it’s going to be commoditized.”

Ken Goldberg, a professor of robotics at UC Berkeley, is less sanguine. When I described Lee’s plan to him, he was blunt. “That’s science fiction,” he said. “In a lab, you need dexterity. You’re manipulating delicate things—materials, crystals, even animals. We don’t understand how to replicate human dexterity. We’re not even close.”

When I pressed Lee on Goldberg’s timeline, she walked it back. Humanoids in three years didn’t mean robots that could match every human movement, she said. On full human dexterity, she conceded, she’s closer to Goldberg—five to 10 years, not three. Medra, she implied, is starting with the easier lab work first.

Nathan Lepora, a roboticist at the University of Bristol, was blunter still. “Developing a humanoid robot doesn’t solve robotic hands and robotic dexterity,” Lepora told me. “You don’t need a humanoid in the lab—what you actually need is robots with the manual dexterity of humans. It doesn’t have to be on legs; it could be some arm coming from the ceiling with a hand on it.” Humanoids, he said, are “important for generating investor interest, generating excitement and public awareness. But humanoids do not solve manual handling dexterity—they’re just a way of transporting hands to where they’re needed.”

What would it take to solve robot dexterity? Even if mouse brain surgery is out of reach, can robots be useful in labs soon? The answer depends on understanding what dexterity actually is, and why it has proven so difficult to replicate.

**The History of Human and Robot Dexterity**

In the second century, the Roman physician Galen, drawing on dissections of pigs and apes and his experience treating gladiators, called the hand “the instrument of instruments”—a phrase he borrowed from Aristotle.

Galen argued that reason without a hand would remain infertile. His intuition ran deep: The hand owed its power not just to its opposable thumb, but to its density of feeling and control. Intelligence, in this view, required an interface with the world that could feel as well as act.

In the 16th century, Andreas Vesalius stripped Galen’s account of its metaphysics while preserving its mystery. In _De humani corporis fabrica_ , Vesalius traced nerves as they fanned into the hand and fingers, dividing and subdividing with a density unmatched elsewhere in the body. He could not explain what this excess wiring accomplished, but he put it on the book’s frontispiece.

Three centuries later, the Scottish surgeon Sir Charles Bell supplied the missing insight. Movement and sensation, he showed, are inseparable. The hand senses by acting: To perform fine motor control, it must palpate what it wants to understand. “It is in the human hand,” Bell wrote, “that we have the consummation of all perfection as an instrument.”

That perfection became measurable in the 1830s, when the physiologist Ernst Heinrich Weber demonstrated that the fingertips can distinguish points separated by just a few millimeters—an order of magnitude finer than most of the body. A century later, the neurosurgeon Wilder Penfield supplied the other half: By stimulating the exposed cortex of awake patients, he showed that the hand occupies a vastly disproportionate region of the brain’s sensory map. Human dexterity is as much sensation as movement: Sensation puts the fine in fine motor control.

“The human hand has something like 15,000 sensors,” Ken Goldberg told me. “All tuned to different pressures, frequencies, and deformations. And we don’t even fully understand how they work together.”

Lepora, who has spent years developing tactile sensors and studies touch from both a neuroscience and engineering perspective, framed it in evolutionary terms. “Bipedalism freed up the use of our hands,” he told me, “and that was part of the process of humans gaining intelligence. The capabilities to manipulate the world, to control the world, to re-sculpt the world in the way that we want—that’s a uniquely human thing. And it ultimately stems from the capabilities of our hands.” If you consider the hand as the cornerstone of human intelligence, he argued, “of course it’s going to be one of the hardest problems to solve in AI and robotics.”

![](https://lede-admin.nautil.us/wp-content/uploads/sites/70/2026/06/pq-03_2f2213.png?w=710)

Grace Chahyadinata, the neuroscience graduate student, encounters this problem every time she operates. “Part of what’s difficult is the targeting,” she told me, “where we’re using landmarks on the mouse’s skull as a proxy for where a particular brain region should be. But none of this is precise.” She adjusts based on what she sees and feels—the slight asymmetry of a skull, the unexpected angle of a suture. “In that sense, it would be hard to do if you’re just seeing it.” That’s the gap roboticists have been trying to close for 60 years.

As early as 1966, researchers at MIT were trying to build tactile sensors that could relay a sense of touch to human operators controlling remote manipulators. Marvin Minsky, the AI pioneer, knew this from the start: Understanding human intelligence would mean replicating our dexterity. He proposed building machines with “visual and tactile input devices capable of unusual discrimination ability.” But the engineering didn’t cooperate. “In attempting to make our robot work,” Minsky later reflected, “we found that many everyday problems were much more complicated than the sorts of problems, puzzles, and games adults considered hard.” This observation anticipated the Moravec paradox: The things that seem easy for humans—perception, movement, touch—are often the hardest for machines.

In 1980, Minsky popularized the term “telepresence” in _Omni_ magazine, calling for machines that would “feel and work so much like our own hands that we won’t notice any significant difference.” Yet he saw a striking asymmetry: “Very little is known about tactile sensations. It seems quite ironic that we already have a device that can translate print into feel,”—that is, Braille—”but we have nothing that can translate feel into feel.” Forty-six years later, it’s still true.

In the 1980s and early 1990s, tactile robotics drew real research attention. Engineers explored every transduction mechanism they could think of: piezoelectric materials that generate voltage when squeezed, capacitive arrays that sense pressure through changes in electrical charge, piezoresistive films whose conductivity shifts under load. Each had its weakness. Piezoelectric sensors excelled at detecting vibrations but struggled with steady forces. Capacitive arrays offered good resolution but were sensitive to temperature and humidity. Worse, commercial tactile sensors cost thousands of dollars and remained fragile, finicky, and difficult to integrate with robot hands.

Then came the “Tactile Winter,” a slowdown from roughly 1995 to 2010, when academic interest in tactile sensing declined even as robotics research overall expanded. As one 2008 survey put it, “Tactile sensing has been a component of robotics for roughly as long as vision. However, unlike vision, tactile sensing always seems to be a few years away from widespread utility.” The same authors identified the core problem: “There is no tactile analog of the CCD or CMOS optical array.” Vision had benefited from decades of camera development, standardized image formats, and—eventually—the massive datasets of the internet. Touch had none of this infrastructure.

In the past decade, a new approach has emerged: vision-based tactile sensing. The insight: Instead of trying to invent new transduction mechanisms, use a camera to watch what happens when something deforms a soft surface. GelSight, invented at MIT in 2009, coats a clear elastomer gel with a reflective membrane. When an object presses against it, the membrane deforms to take the object’s shape. Colored LEDs illuminate the surface from different angles, and a camera captures the resulting shading patterns. Photometric stereo algorithms then reconstruct a three-dimensional map of the contact with sub-millimeter resolution. The sensor sees touch.

This transmogrification of touch into vision has revived the field. Deep learning pipelines developed for image recognition can be repurposed to extract force, texture, and slip information from tactile images. Meta AI partnered with GelSight to develop DIGIT, a small, low-cost tactile fingertip released in 2021 with open-source designs. The latest version, DIGIT 360, packs 18 sensing modalities into a fingertip-sized package—force, geometry, vibration, temperature, even chemical signatures—and includes an onboard AI chip for reflex-like local processing. Other fun-named variants have proliferated: GelSlim, TacTip, Soft-bubble, OmniTact, each optimizing for different trade-offs of size, durability, and resolution.

**The Sense of Touch in Today’s Robots**

I was surprised to learn that none of the foundation models for robotics include touch as a sensory input. These models—large, pre-trained control policies—combine vision, language, and proprioception to generalize across many manipulation tasks. Proprioception—the robot’s awareness of its own joint positions and forces—has become standard in nearly all top models, since it helps close the loop between what the robot sees and where its limbs actually are.

Google’s early RT-1 model, from 2022, relied solely on visual input, but its successors quickly added internal state sensing. DeepMind’s RoboCat, released in 2023, tokenizes both camera images and joint positions, enabling a single transformer to control multiple robot arm designs across more than 250 tasks. PaLM-E, Google’s 562-billion-parameter embodied language model, combines what the robot sees with continuous estimates of its own state, letting it reason about reachability and force constraints.

But touch is missing from most of these systems, in any form. Of the major foundation models released through 2024—RT-1, RT-2, Gato, RoboCat, PaLM-E, OpenVLA, Octo—none incorporated tactile sensing. The reasons go deeper than hardware.

This absence matters because dexterity is a control problem under uncertainty. A robot rarely knows the exact pose, friction, compliance, or contact geometry of what it’s manipulating; the moment it touches the world, the world pushes back. Without tactile feedback, the controller is flying blind during the most critical milliseconds—when slip begins, when a pipette tip hits plastic instead of air, when a mouse’s skull gives way slightly under a drill. Vision can tell you where things are, but only touch can tell you what’s happening at the moment of contact.

Yet vision-based tactile sensing has a problem of its own: labeling. You can fine-tune a vision model on tactile images, but how do you label them? Basic tactile images you might label. The fine distinctions get out of hand. “This is the image I get when I touch an apple; this one when I touch a fuzzy peach; this one when I touch a nectarine, which feels like a peach but not quite; this one when I squeeze that nectarine hard.” The distinctions that matter for manipulation are endless and subtle, and there is no crowd of internet users casually annotating them the way they do for photographs of cats.

Lee, for her part, is confident the field will solve it soon. “They all know this is a problem across all industries,” she told me.

In January 2026, Figure AI unveiled Helix 02, a humanoid robot model whose control policy fuses head-camera images, wrist and palm camera views, fingertip tactile sensor readings, and the robot’s entire joint state into a single neural network. Helix enabled Figure 03—the company’s flagship humanoid—to pick up individual pills, handle tiny objects, and perform “long-horizon” tasks like unloading a dishwasher. The demos showed feats that would be near impossible with vision alone. (NEO, a humanoid from the start-up 1X, also includes tactile sensors in the hands, though I haven’t seen any dexterity demos, and the few journalists who have seen NEO in action have been less than impressed.)

![](https://lede-admin.nautil.us/wp-content/uploads/sites/70/2026/06/pq-04_86e47d.png?w=710)

One recent demonstration challenged the idea that dexterity without touch is impossible. In late 2025, the startup Physical Intelligence—a San Francisco company that has raised over $400 million to build “foundation models that can control any robot”—swept a set of benchmark tasks designed by the roboticist Benjie Holson to test humanoid dexterity. Holson, who writes the newsletter General Robots and had visited Physical Intelligence’s headquarters, had expected some of the tasks to take a year or more to solve. Physical Intelligence claimed them all in three months.

The tasks were deliberately chosen to seem out of reach: spreading peanut butter on bread, turning a sock inside out, inserting and turning a key, peeling an orange without tools. “When I selected the tasks I tried to think of things where I thought current approaches would not work,” Holson wrote. “Tasks like peanut butter spreading or wiping glass need force feedback. Tasks like key manipulation or sock inversion need dextrous many-fingered hands.” He was wrong on all counts. Physical Intelligence solved them with standard cameras and simple pincer grippers. No tactile sensing required.

Holson’s conclusion: “If we continue to find that vision is ‘good enough’ to keep solving harder and harder tasks, that would make useful manipulation a data collection problem—not an invention problem.”

There’s precedent for this kind of shortcut. Human neurophysiology is staggeringly complex—86 billion neurons, each forming thousands of synaptic connections, with dynamics we still don’t fully understand. And yet the artificial neurons that now power large language models and image generators are crude by comparison: simple algebraic summation and thresholding, inspired by real neurons but just a shadow of their intricacy. That caricature turned out to be enough to summon something that looks like intelligence. The same may prove true for robotics. Perhaps vision, data, and scale will be enough to get us to dexterity—even if the underlying mechanisms look nothing like the human hand.

Lepora remains skeptical. I asked if human-level dexterity will require tactile perception. “It’s a trillion-dollar question,” he told me. “There are companies invested in the paradigm that vision plus proprioception is enough, plus enormous amounts of AI. And there are some really impressive demonstrations being done.” He paused. “But look—how would we work without a sense of touch? We couldn’t do anything, could we?” Betting everything on vision, he said, “is not a safe bet, for sure. It might be there’s a limit, and you get diminishing returns.”

If anything tips the scales for Lepora, it’s the ability to use tools. Tool use is a hallmark of intelligence—something that separates humans from most animals. And while a creature needs brain power to even think to use a tool, actually using one is a different problem; for that, you need dexterity. Perhaps that’s why corvids, for all their intelligence, haven’t gotten much past turning sticks into hooks. So far, the robots haven’t fared much better. “I haven’t seen any of those things do proper tool use,” Lepora said. “That’s the archaeological record, what we measure human evolution by: the tools that we make, use, and leave behind. Will these vision-based techniques be able to get to that point?”

That’s the open empirical question, and it will be answered by data and engineering, not by argument. Whether robots can spread peanut butter without crushing the bread is the kind of problem the field knows how to attack. The harder question—the one that has nothing to do with hands—is what happens to scientific judgment when the manual drudgery scientists currently endure is taken away. ![](https://assets.nautil.us/sites/3/nautilus/nautilus-favicon-14.png?fm=png)

_[This article](https://oftwominds.substack.com/p/the-instrument-of-instruments-why) originally appeared on “[Of Two Minds](https://oftwominds.substack.com/),” a Substack blog about natural and artificial brains by Grigori Guitchounts and Jesseba Fernando._

_Lead image: Tasnuva Elahi; with images by Marina Zlochin and Happypictures / Adobe Stock_
