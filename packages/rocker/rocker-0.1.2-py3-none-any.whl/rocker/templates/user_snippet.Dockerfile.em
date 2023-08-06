# make sure sudo is installed to be able to give user sudo access in docker
RUN apt-get update \
 && apt-get install -y \
    sudo \
 && apt-get clean

@[if username != 'root']@
RUN useradd -U --uid @(user_id) -ms /bin/bash @(username) \
 && echo "@(username):@(username)" | chpasswd \
 && adduser @(username) sudo \
 && echo "@(username) ALL=NOPASSWD: ALL" >> /etc/sudoers.d/@(username)
# Commands below run as the developer user
USER @(username)
@[else]@
# Detected user is root, which already exists so not creating new user.
@[end if]@