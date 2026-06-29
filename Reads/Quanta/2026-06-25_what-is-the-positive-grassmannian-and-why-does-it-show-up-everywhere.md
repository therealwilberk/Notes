# What Is the Positive Grassmannian and Why Does It Show Up Everywhere?

**Source:** Quanta  
**Author:** Janna Levin and Steven Strogatz  
**Date:** 2026-06-25  
**Link:** https://www.quantamagazine.org/what-is-the-positive-grassmannian-and-why-does-it-show-up-everywhere-20260625/

---

**STROGATZ:** Okay. And this word “orthant,” which isn’t totally familiar, is the 3D version of quadrant.

**WILLIAMS:** Exactly.

**STROGATZ:** Right. There’s eight of them. So that’s why you’re saying “orthant.”

**WILLIAMS:** Yeah. So that positive orthant would be where the X, Y, and Z coordinates are all positive or non-negative.

**STROGATZ:** Okay. And you say it looks sort of like a curvy triangle. And so at this point, if people are still with us, why would anyone think about this object? This doesn’t seem like an obvious thing to think about.

**WILLIAMS:** Yeah, yeah. It wasn’t an obvious thing to think about, but back in the 1900s, mathematicians were studying certain kinds of matrices called totally positive matrices, and they had nice properties. They had some connections to different systems like oscillation.

And then in the late 1990s, early 2000s, Lusztig and Postnikov realized that there was a way to sort of generalize this notion of totally positive matrices to an object that lived inside the Grassmannian. And so it was just sort of a purely interesting mathematical idea to try to study total positivity, not just for matrices anymore, but for geometric objects like the Grassmannian.

So, there’s all kinds of sets of matrices that describe motions and symmetries for the real world.

**STROGATZ:** And they come up in quantum theory. They’re used all the time now in artificial intelligence, but even inside of math, as you say, they’re, they can act like machines that do things to other mathematical objects.

**WILLIAMS:** Yes, in math, one of the common themes is that we study not just the mathematical objects, but also the relationships between the objects. And matrices can give us a way to create or to analyze relationships between different mathematical objects.

**STROGATZ:** Now, one of the results that you are known for was this positive Grassmannian that we talked about, you looked at in a combinatorial way, in the very general case. So, tell us a little bit of the flavor of what you did there.

**WILLIAMS:** Yeah, absolutely. Back when I was a grad student or postdoc, I think I had a conversation with some other mathematicians about, you know, just what combinatorics is as a field. and one thing that we discussed at that dinner was that one can think of combinatorics, not necessarily just as a field, but as an attitude.

You know, we can go through life, uh, with a combinatorial attitude and take a combinatorial approach to different problems. And the positive Grassmannian can be divided into pieces of different dimensions. An analogy I like to use is that of the cube, say the three-dimensional cube. If a combinatorialist looks at it, they may come away saying, “Well, it has six two-dimensional faces,” these squares on the different sides, “and it has 12 one-dimensional edges, and it also has eight zero-dimensional pieces,” the eight vertices.

And so you can associate these numbers, six, 12, and eight to a cube. That’s what a combinatorialist might do. Now, there are infinitely many positive Grassmanians, and they can have arbitrarily high dimension, but the first problem that I worked on in graduate school was coming up with an explicit formula for how many pieces there are of each dimension.

So, I wrote down a polynomial that for any k and n tells you how many pieces there are of each dimension in that positive Grassmannian.

**STROGATZ:** Okay, so let’s now make a little swerve from this pretty abstract realm of matrices and Grassmannians and positive Grassmannians to the much more mundane world of traffic and waves on the ocean and proteins being made inside of cells, because it turns out all those things can be viewed as part of one story.

I was floored when I saw this paper to think that my polynomials had to do with a sort of, quote-unquote, ‘real world.’

**WILLIAMS:** That’s right. There have been sort of three different areas that I’ve had personal experience with where the positive Grassmannian got connected. During my postdoc, I learned that another mathematician, Sylvie Corteel, had written a paper which said that my polynomials that were counting pieces of the positive Grassmannian according to dimension were also computing probabilities in a model that had been introduced to study translation in protein synthesis and was also used as a model for traffic flow.

I was floored when I saw this paper to think that my polynomials had to do with a sort of, quote-unquote, “real world.” Her result was quite beautiful. Basically, she was saying that my polynomials were giving the probability that in a lattice with n sites or in a road with space for n cars, there are exactly k cars present. That’s what my polynomials were computing.

So great, so we know the probability that in a road with space for n cars, there’s exactly k present. Well, what if we want to know the probability that the cars are present in positions one, four, five, eight? You know, what if you want to know all the probabilities that any given configuration of cars is there? And so that was the natural question to ask. That actually kicked off a decades-long collaboration with Sylvie. I mean, we’ve written a number of papers together by now.

[_Music plays_]

[**STROGATZ:** So, there’s a lot to unpack there, Janna. Did that wash over you?

**LEVIN:** Well, I mean, I grasp some of it, right? This idea that you can cut some mathematical object into pieces, find some mathematical rule for the number of pieces occurring of a certain variety. She was saying dimensionality. So having heard all of that, which is very intriguing, just give me the bird’s-eye view of what a Grassmannian is.

**STROGATZ:** Okay, fair enough. Right, it’s not a concept we run into every day. So here’s what it is. There’s a technical way we could define it, but before I give you that, can I give you ‘What’s it gonna do for us?’ How is it helpful? So, it’s a really nice meta-concept. It’s a shape that tells us about other shapes.

**LEVIN:** Hmm.

**STROGATZ:** It’s a shape that can be used as a library or a catalog for other kinds of structures or shapes.

**LEVIN:** So it’s one shape or it’s a family of shapes?

**STROGATZ:** It’s a family of shapes. There’s different Grassmannians. I mean, here’s the technical definition, which may work for you, but I don’t wanna linger on it too long because I don’t think it’s the most helpful way to think about it.

Technically, it has to do with thinking about all the different ways that k-dimensional spaces, linear spaces, like a two-dimensional space would be a plane, a one-dimensional space would be a line, a three-dimensional space is what we’re used to for ordinary 3D space. Yeah. So you’re trying to think about the totality of all k-dimensional linear spaces through the origin of n-dimensional space.

**LEVIN:** Okay.

**STROGATZ:** So there’s two parameters, k and n. Now, the simplest case would be think about lines through the origin. That’d be one-dimensional spaces through the origin in a plane.

**LEVIN:** So n is two, k is one.

**STROGATZ:** Right. That would be the 1-2 Grassmannian or something like that.

**LEVIN:** Oh, I see. Okay.

**STROGATZ:** Okay? So there’s, infinitely many, a whole continuum of lines, but if you wanted to parameterize them in our language, if you wanted to catalog them, you could do it by saying, “What’s their compass direction?” Like there’s the line that goes north-south, or there’s the line that goes north-northeast and south-southwest or something like that, right? So if I listed all of those possible lines, it could be the whole upper semicircle. So that’s a shape.

**LEVIN:** And so people study different Grassmannians, some high-dimensional space and some lower dimensional.

**STROGATZ:** Exactly. Now, Lauren specializes in this piece of it that’s called the positive Grassmannian, which in our little example with lines through the origin in the plane would be like only considering the ones that have positive slope. And that turns out to have extra structure that makes it more helpful in lots of applications.

At this point, it seems like something that pure geometers would think about. This is about a shape that classifies other shapes. The spooky thing is that this pops up all over the place in real-world settings. So like she mentions, traffic flow. I want you to have not an image of cars motoring down the highway, ’cause she doesn’t really mean that kind of traffic.

Think of back when COVID was rampant and we had to stand in line at the checkout for the supermarket, and you had to stay six feet behind the person in front of you, right? So imagine you had something like 10 spots available that you could stand on. That would be like our n. And now people start arriving to get in line and also people at the front of the line can leave, and the rules of the game are that whatever spot you’re on, you have some probability of moving forward one spot, except not if someone’s standing there.

There’s a constraint. If you let this whole thing run for a long time with people arriving at random and leaving at random, and moving forward one spot at random when they can, you could classify all the possible ways that these 10 spots could be occupied by four people, let’s say. That would be the k. It turns out the 4,10 Grassmannian tells me something about the likelihood of seeing a particular number of people in this queue.

**LEVIN:** Now, I’m curious. I can imagine during COVID, as you said, having to solve this problem, right? It’s a problem that has to be solved because we now have distribution centers for vaccines, and this is happening or something like that. How does somebody notice that the polynomial that they’ve generated to answer this practical question happens to be the same as a polynomial a very abstract mathematician has found for a Grassmannian on the positive with positive Grass… I mean, how do they even notice this correlation?

**STROGATZ:** That might be the unique genius of Lauren Williams and her collaborator, Sylvie Corteel. And it’s not just about the queues. If you think about ribosomes moving down an mRNA molecule as they’re doing protein synthesis, it also pops up in that setting. You see what I’m getting at? This is a really fun, diverse set of applications all mysteriously falling under the heading of the positive Grassmannian.

But after the break, Lauren Williams will walk us through why this phenomenon might be happening, why it’s happening so pervasively, and also how artificial intelligence may or may not take over mathematics.

[_Music plays_]

**STROGATZ:** Welcome back to _The Joy of Why_. We’re speaking with Harvard mathematician Lauren Williams about algebraic combinatorics and the positive Grassmannian.

**STROGATZ:** I would love to ask about why these connections to the much more mundane world happen. I know that no one knows.

**WILLIAMS:** Well, you know, what’s really interesting to me is that you know, with the model of traffic flow, it’s this model of particles that repel each other. And with the shallow water waves, these are waves that are sort of coming together and interacting. And with the scattering aptitudes, it’s about particles that are being thrown together and interacting. And somehow it’s always about particles or waves that are being flung together and then they sort of repel in some way.

And you know, the coordinates one uses for the Grassmannian are Plücker coordinates. And if you have your k by n matrix, you think of this as a, as a list of column vectors. Well, if two, two vectors get so close that they’re actually on top of each other, your Plücker coordinate vanishes. So there’s something in the nature of the Plücker coordinates on the Grassmannian that build in this repelling property.

And so I’ve always wondered if it could be possible to connect these three different settings, whether it’s the particles repelling each other, or the waves, or the scattering aptitudes. But somehow I think it all comes down to Plücker coordinates on the Grassmannian.

The Grassmannian is so universal, and then there’s something about positivity that just captures properties of the real world for some reason.

**STROGATZ:** That’s nice. That’s a very, very nice answer. And I mean, it feels like a more refined way of saying what you said at first. ’Cause I’ve seen diagrams like when you look at the particles in the Feynman diagrams, veering towards each other and then bouncing off. Or if you look at the diagrams of the water waves where you’re just looking at, I don’t know what, the crests or something, there’s ways of drawing the pictures that it almost looks like you’re drawing the same picture over and over.

**WILLIAMS:** Right, right, right.

**STROGATZ:** Yeah. So, I mean, it would be weird, then again, maybe not so surprising that if at a very deep level we’re drawing this same picture over and over and nature is interpreting it, or math is interpreting it in different ways in different settings, but it’s kind of the same mechanism. But your, your thing with the Plücker coordinates, and the… does the zero mean that that’s the analog of repulsion. They won’t go through each other because of that zero?

**WILLIAMS:** Well, they could, but then there’s a sign change.

**STROGATZ:** Oh.

**WILLIAMS:** And then somehow, like with the shallow water wave stuff, I was thinking about why positivity comes into the picture. You know, to analyze these solutions, to analyze these water waves, you use Soliton solutions to the KP equation, and that involves a tau function in which you take the log of a certain function, and this function is built out of the Plücker coordinates in some way. And as long as the Plücker coordinates are all non-negative, you’re taking the log of something that’s always positive.

But if you lose this positivity, if you now are talking about all points in the Grassmannian and not just the positive part, you might at some point be taking the log of zero or something really close to zero. But then what happens is that your model for shallow water waves goes off to plus or minus infinity, which obviously does not represent the real world.

And so there’s something about, you know, if you want to stay in the real world, you have to stay away from this zero. And it means restricting to the positive Grassmannian. So, yeah.

**STROGATZ:** But if we were to just get a little sloppier, but I think maybe more understandable about it, is it that there are sort of a bank of possible patterns that can happen in our minds or in nature. And sometimes those patterns just, you know, if they’re fundamental enough, they will show up in many parts of our thought and in our observations.

So like there’s a certain family of patterns that you are swirling around and this positive Grassmannian story is encoding them, and they have different manifestations in math and in the world, but it’s kind of the same pattern over and over.

**WILLIAMS:** Yeah, maybe that’s right. Maybe that’s right. I mean, the Grassmannian is so universal, and then there’s something about positivity that just captures properties of the real world for some reason.

**STROGATZ:** This story is not over because then somehow you get entangled, naturally I use that word, with things happening in quantum physics specifically with things related to a very beautiful quantum field theory: N=4 supersymmetric Yang-Mills theory.

**WILLIAMS:** Yes, yes.

**STROGATZ:** If I’ve got that right. But anyway, Nima Arkani-Hamed and other collaborators are looking at this fantastic model and somehow you connect to them. You want to build that bridge for us?

**WILLIAMS:** Yes. So they started to realize that somehow the structure of the positive Grassmannian was helping to understand scattering amplitudes. So scattering amplitudes are basically probabilities that tell you what you might expect would happen if you throw a bunch of particles with given momentum together and more particles come out.

Well, I guess that sort of classical approach to scattering amplitudes was to use some complicated diagrams called Feynman diagrams. But the physicist Nima Arkani-Hamed and collaborators realized that there were more compact ways to understand these scattering amplitudes. And they involved a lot of the machinery of the positive Grassmannian. Um, yeah. And then this in turn led to a beautiful geometric object that they call the amplituhedron, whose volume computes scattering amplitudes.

**STROGATZ:** Before we start delving into the amplituhedron, if I’m saying that right, I, there was one question I had about something in, in doing a little background reading that you mentioned, these Feynman diagrams. It’s a wonderful technique for calculating the kinds of information that physicists need to try to match what they see in their experiments or to make predictions about future experiments. But it can be very arduous. There could be thousands of diagrams, sometimes even more that they have to calculate on computers.

And the crazy thing that seems to have come out in the amplituhedron story, as done by the physicists, is that the thousands of calculations can be reduced sometimes to one calculation.

That is, when you mention calculating a volume, it’s analogous to finding a volume of a shape. And it seems like a miracle. How could a thousand or a million things be replaced by one thing? And it reminded me of cancellations that I teach when I teach calculus. There’s something we teach and you probably have to teach calculus from time to time too. We talk, call it a telescoping series where there’s a series of terms and then on the inside there’s a lot of things being added and then subtracted again and added and subtracted and they all collapse. And I feel like from what I read, that in your picture you, ’cause we talked about positive as an adjective applied to the Grassmannian, that when you have this positivity extra thing thrown in there, it somehow gives rise to this kind of, it’s not the same cancellation as in a telescoping series, but it feels like it has that flavor.

A lot of internal cancellation simplifying a big messy thing to something much simpler. Am I on the right track with that? I mean, even morally, if not in detail.

**WILLIAMS:** So, there are many cancellations that occur when one goes from kind-of Feynman diagram expressions to the sort of most compact expressions that we know.

A big advance in this area was the recurrence of BCFW, Britto, Cachazo, Feng, and Witten, and they wrote down this beautiful and much more compact recurrence for computing scattering amplitudes. And then what was noticed a few years later by a physicist named Hodges was that in some special cases, if you take the recurrence and you express your amplitude as a sum of terms, it looked like the sum of terms was computing the volume of some geometric object by cutting it into pieces and adding up the volumes of those pieces.

So, this was an observation of Hodges in a few very special cases, and then he asked the question, “Is this true in general?” Can we write all of these scattering amplitudes as computing volumes of some geometric object by cutting them up into pieces and summing them up? So Nima Arkani-Hamed and Jaroslav Trnka invented/discovered the amplituhedron as the answer to this question.

So they defined this object, and it’s closely related to the positive Grassmannian, and they proposed in their 2013 paper that this was the answer to Hodges’s question. The volume of this object is indeed computing the scattering amplitudes in question.

**STROGATZ:** So, maybe we should close our discussion here by just going into a little bit of what you’ve been doing very recently, in connection with a project known as First Proof. Can you fill us in on what this project is about and what you’re trying to do with it?

**WILLIAMS:** Yeah. So First Proof is a project that we initiated in the fall, and the motivation and the idea was to try to come up with an objective measure of how good AI systems are at coming up with proofs of mathematical statements. There’s been a lot of noise in the media either sort-of hyping up the ability of AI or denigrating it, and we thought mathematicians themselves should try to figure out how best we can use AI in our own research, and in particular, to figure out how good AI is at coming up with proofs of statements.

But this is a very tricky thing to test because LLMs, AI models are extremely good at searching the literature. So, if you ask your favorite AI model to come up with a proof of a mathematical statement, if that statement and proof are on the internet somewhere, it’s gonna find it. So we wanted to know how good is it at coming up with new proofs that aren’t already out there.

And so what we decided we needed to do was take mathematical statements, lemmas, say from our own research, where we had proved the lemma or the statement, but we had not released the solution on the internet anywhere, and propose these kinds of statements as problems, as a challenge for AI systems. So, a group of 11 of us got together and produced these kinds of problems from our work and put them out on the internet in a paper on February 6 as a challenge for AI systems.

**STROGATZ:** That’s February 6th, 2026 for people in the future listening to this.

**WILLIAMS:** That’s, that’s right. Yes. And then what we did at the time was we wanted to sort-of make clear that we had solved these problems ourselves. We encrypted our solutions, we put the encrypted solutions on the internet, and then we said that we would release the key to the encryption, we’d release the solutions, publicly in one week’s time.

And so during that time, we were really gratified to see that there was just an incredible amount of interest, both from the mathematical community, like professional mathematicians or math afficionados, but also from the big AI companies, you know, jumping on the challenge and seeing what they could do.

**STROGATZ:** Yeah. ’cause these are not like the Olympiad problems or the high school math contest problems or anything like that. These are really research-level questions, but bite-sized.

**WILLIAMS:** That’s right.

**STROGATZ:** As you say, they’re lemmas, not the whole paper.

**WILLIAMS:** Right, right, right. So this was a new kind of challenge because as you said, most previous benchmarks consisted of problems with numerical answers, as opposed to answers that consisted of proofs. So with all of our problems, we made sure that we had proofs that were roughly five pages in length, or less.

**STROGATZ:** And how did the AIs do? Is it possible to assess?

**WILLIAMS:** Yeah, so we did our own private assessments at the time that we came up with these 10 questions. And, actually deciding the protocols around testing is also a tricky thing to do because you could give an AI model one shot to answer the question. You know, you could just give it the problem and see how it does. Or one could have an extended conversation with the model and try to coax it to give a better answer. But so in our private tests that we did beforehand, we just gave each AI model one shot to answer the question. We didn’t have any back and forth, and what we found at that time was that the models could solve two of our 10 questions.

**STROGATZ:** Oh, okay. That’s not bad. These are hard questions.

**WILLIAMS:** Yeah, yeah, yeah. No. Not bad. And during that week various individuals and also people with the companies were working on the problems and coming up with solutions. And if you sort-of put together the best efforts from all of the different people and groups who submitted answers, we did get perhaps correct solutions to six of the 10. But we are trying to shy away from making any formal statements about how people or groups did because we didn’t lay any ground rules. Since different people and different groups and different companies would’ve had different procedures, and different amounts of feedback, it’s hard to sort of compare how the models did.

**STROGATZ:** And so now you have very recently, it was only a few days before our conversation right now, you released what you’re calling, what are you calling it?

**WILLIAMS:** The second batch.

**STROGATZ:** The second batch.

**WILLIAMS:** Yes. First Proof is a baking pun. It’s about proofing the dough before you bake it. And so we put out, you know, our first batch of problems back in February and just a few days ago on March 14, 2026, on Pi Day, we put out an announcement that we will release a second batch of problems sometime later in the spring. They will similarly be sort of bite-sized problems from different areas of mathematics coming from research of mathematicians. But this time we mean for our problems to be a more formal benchmark. And we do intend to get the solutions graded at the end.

**STROGATZ:** Okay. Well, this’ll be interesting to see. Are there any discoveries about either of the things we really talked about the Grassmannian and its relatives, or this AI work, you most hope to see, say 10 years from now?

**WILLIAMS:** As far as the Grassmannian goes, I’m hopeful that maybe there’s even more exciting connections to other parts of the real world. And as far as the AI model go, it’s very hard for me to predict. You know, it feels like the ecosystem in which we’re doing math is being upended and we’re trying to figure out how best to adapt, how we can use these new tools. I would hope that 10 years from now, they would be sort of research partners, with a sort of higher level of reliability and confidence than we have at the moment.

**STROGATZ:** All right, and the last thing, is there something you could put your finger on that particularly is a source of joy for you as a mathematician? What brings you joy in your work?

There’s been a lot of noise in the media either sort-of hyping up the ability of AI or denigrating it, and we thought mathematicians themselves should try to figure out how best we can use AI in our own research, and in particular, to figure out how good AI is at coming up with proofs of statements.

**WILLIAMS:** I think it’s identifying connections between things I didn’t expect to be connected. You know, just finding these kinds of connections, whether it’s to the traffic flow, or to the shallow water waves, or to the scattering aptitudes. I have so many stories from my research where I might have a conversation with another mathematician and they show me some numbers of something that they were computing, and then I recognize them as having come up before. It’s always so exciting and intriguing. I mean, it’s this sort of mystery and then we have to do the detective work of figuring out how these objects are connected.

Yeah, so I think that’s the thing that I find most exciting. And then of course, the joy is when you realize, you make that connection. You understand, you have this realization of how they are secretly connected and how you can sort of make that rigorous.

**STROGATZ:** Well, very, very good. It’s really been fun. Thank you, Lauren.

**WILLIAMS:** Thank you, Steven

[_Music plays_]

**LEVIN:** Wow. So this is terrifying, right? Now, I really do wonder, hey, have I written the last of my very, very technical papers. But then I also remember the time that computers were first invented, and everybody was saying … that’s not… I don’t remember when computers were first invented. But you know what I’m saying. When they got cheaper, more readily available, large processing machines could do huge datasets, and the same kind of thing was said: “Well, now the technical people are obsolete.” I don’t know. What do you think?

**STROGATZ:** Well, um, I’m confused about it. I really am of two minds, and, you know, we still have CAPTCHA, that thing where you have to identify that you’re not a robot by doing some little image processing. Apparently, that’s still hard for the AIs. So yes, they’re very good at certain things, but there’s still a way to go. They also seem to lack common sense in a lot of domains. But still, back to your question though, I mean, will they make you and me and people like us obsolete? Because what we do isn’t exactly the realm of common sense. We’re in a… as my wife would be the first to tell you.

**LEVIN:** Right, exactly. And she’d be right.

**STROGATZ:** No, but you know, like a lot of the work we do involves very explicit rules. You could imagine we might be at risk more than the people who do plumbing or caregiving, who will be the last to be superseded by robots and AIs.

**LEVIN:** Well, just to play devil’s advocate, I think the idea of these machines as thought partners is closer to what I’m imagining is going to happen, because I still don’t see the machine asking the questions.

**STROGATZ:** Not yet, no. Do you think in the era when AI starts doing math alongside us, or maybe even instead of us, will beauty play the same role then? Like a guide to what you should think about, what questions you should ask, how to judge whether you’re on the right track with the theorems you can obtain.

**LEVIN:** Gosh, it’s a really… profound question, ’cause one of the roles beauty might be playing is rendering some very complex subject comprehensible to us. Which I really need because I don’t have infinite compute. So, I need to have a more aesthetic approach.

So, I mean, you could kind of say, in a way, nature already has all the answers. The whole game is discovering what nature already knows. So, if the AI just simply has this infinite list of things it knows, you know, if we don’t understand it, I don’t know that the game has changed that much. I don’t know. What do you think?

**STROGATZ:** I always wonder about is understanding overrated? So, here’s what I mean, that we might be confusing means and ends. Like, if the end is to predict nature, to be able to find formulas and theorems that are true, understanding may be a crutch. It helps us get good answers. It helps us get more control over the universe, but it’s not the game.

Like, if you’re trying to save someone’s life, you may have to come up with a medical therapy that you don’t understand that works. And so it’s not always so clear to me that understanding is the goal in itself.

But on the other hand, there are people who say it’s not science without understanding. It’s something less than science. It’s like a degradation of the human spirit. Why even do it if you’re not understanding? I don’t know what to think about that. I can see both sides of that argument.

But what’s really interesting in what Lauren Williams and her colleagues are doing is they are giving these secret problems from research-level math that haven’t been published, so the AI can’t look them up on the internet, and asking them how many of our 10 problems can you solve? It’s just an interesting benchmark, different methodology than we’re seeing elsewhere.

**LEVIN:** Yeah. Yeah, it’s amazing ’cause it means they’re not just regurgitating, culling a human response.

**STROGATZ:** So far they’re not mastering that. They’re not climbing the whole mountain.

**LEVIN:** But right now, in the context of what people are doing, is it possible to have a machine that says, “You know, here’s an interesting idea,” or, you know, “I’m bored today I’m going to try this,” or…

**STROGATZ:** We’ll really know that they’ve arrived when they’re a guest on _The Joy of Why_.

**LEVIN:** Yeah. When we have Claude on.

**STROGATZ:** Yeah, when we have Claude, and course, by then, maybe we won’t be the hosts anymore.

**LEVIN:** Yeah. Oh, man.

**STROGATZ:** But until then…

**LEVIN:** Until then.

**STROGATZ:** See you later, Janna.

**LEVIN:** If you’re enjoying _The Joy of Why_ and you’re not already subscribed, hit the subscribe or follow button wherever you’re listening. You can also leave a review for the show. It helps people find this podcast. Find articles, newsletters, videos, and more at quantamagazine.org.

**STROGATZ:**  _The Joy of Why_ is a podcast from _Quanta Magazine_ , an editorially independent publication supported by the Simons Foundation. Funding decisions by the Simons Foundation have no influence on the selection of topics, guests, or other editorial decisions in this podcast or in _Quanta Magazine_. _The Joy of Why_ is produced by PRX Productions. The production team is Caitlin Faulds, Jade Abdul-Malik, Genevieve Sponsler, and Merritt Jacob. The executive producer of PRX Productions is Jocelyn Gonzales. Edwin Ochoa is our project manager.

From _Quanta Magazine_ , Simon Frantz and Samir Patel provided editorial guidance, with support from Samuel Velasco, Simone Barr, and Michael Kanyongolo. Samir Patel is _Quanta’s_ editor-in-chief. The episode art is by Chanelle Nibbelink, and our logo is by Jackie King and Kristina Armitage. Special thanks to Garth Avery at the Cornell Broadcast Studio.

I’m your host, Steve Strogatz. If you have any questions or comments, please email us at [[email protected]](https://www.quantamagazine.org/cdn-cgi/l/email-protection).
