
if [ "$TRAVIS_PULL_REQUEST" == "false" ]; then
  echo -e "Starting to update test-travis repo\n"

  #copy data we're interested in to other place
  cp -R coverage $HOME/coverage

  #go to home and setup git
  cd $HOME
  git config --global user.email "test@local.fr"
  git config --global user.name "zimoun-Travis"

  #using token clone gh-pages branch
  git clone --quiet https://${GH_TOKEN}@github.com/zimoun/test-travis.git > /dev/null

  #go into diractory and copy data we're interested in to that directory
  cd test-travis
  cp -Rf $HOME/coverage/* .

  #add, commit and push files
  git add -f .
  git commit -m "Travis build $TRAVIS_BUILD_NUMBER pushed to gh-pages"
  git push -fq origin master > /dev/null

  echo -e "Done magic with coverage\n"
fi
