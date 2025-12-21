FROM jekyll/jekyll:4
WORKDIR /srv/jekyll
COPY . /srv/jekyll
RUN bundle config set path /usr/local/bundle && bundle install || true
CMD ["jekyll", "build", "--destination", "_site"]
