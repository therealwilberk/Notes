# n8n Setup & Workflows
> Workflow automation — self-hosted via Docker

## Setup Status
- [ ] Install Docker (`sudo pacman -S docker docker-compose`)
- [ ] Start Docker service
- [ ] Deploy n8n via Docker Compose
- [ ] Configure persistent volumes
- [ ] Set up webhook endpoints

## Feeds to Monitor

### Blog.Nevine.Me (Kenya Jobs/Internships)
- **URL:** https://blog.nevine.me
- **Feed:** `https://blog.nevine.me/feeds/posts/default`
- **Type:** Atom (Blogger)
- **Posts:** 6,480+
- **Categories:** Jobs, Internship, Engineering, Kenya, career, tech, IT
- **Author:** Ruth N.
- **Use case:** Monitor for EE/internship job postings
- **n8n node:** RSS Feed Trigger → Filter by keywords → Notify

## Planned Workflows
- [ ] Job feed monitor (blog.nevine.me + others)
- [ ] More TBD after n8n is live
