# SmartMeetings: Product Requirements Document
### Team Name: Meeting is Believing
Team Members: Maxton Ginier (Lead), Tuan Le, Jackson Li, Sarita Phoosopha, Christina Tao

## Introduction
### Problem
Meetings are crucial for any line of work. They are absolutely necessary for communication between colleagues about ideas, problems, roadblocks, etc… However, repetition of discussions and materials from previous meetings are downfalls that cause present-day meetings to be very inefficient and leads to more unnecessary meetings. Other common problems in meetings are undistributed speaking time, downfalls of groupthink, members absence, and run on meetings.
### Innovation
This project will produce a tool that makes meetings more productive and collaborative by providing a more meaningful analysis of the meeting. This will be accomplished by displaying and maintaining specific scrum information to detect progress. The application will prompt pre-meeting questions about the type of meetings (stand-up, long board meetings, etc.) and the estimated/desired meeting time that the application will use to predict how the pacing and runtime of the meeting. Additionally, video analysis will be used to detect restless/anxious behaviors (e.g. fidgeting) to inform meeting participants that the meeting may be running too long.
### Core Advancement
Our project aims to solve this problem using machine learning technologies, primarily audio recognition and natural language processing tools to provide annotated transcript, note-taking, and automatic to-do list creation based on spoken keywords. The project also aims to track meetings progress and emotional sentiments of each member as they contribute to provide a well-rounded summary of the meetings.
### Background
The problem is currently being solved using audio transcription by various companies; however, the processing and analysis of the transcription is lacking. Most applications focus on having a simple transcription of the meeting afterwards, which catch absent members up when necessary, but does not access real-time information that can benefit current, as well as the future meetings.

## System Architecture Overview
### High Level Diagram

## Appendices
### Technologies Employed
GUI: React w/ Material UI
RTC: WebRTC
User Database: MongoDB
Audio/Video Storage: Amazon S3
Backend Framework: Ruby on Rails
Web Hosting: DigitalOcean
Audio Transcription: IBM Watson
Audio/Text Processing: nltk (Python)
Container Platform: Docker
