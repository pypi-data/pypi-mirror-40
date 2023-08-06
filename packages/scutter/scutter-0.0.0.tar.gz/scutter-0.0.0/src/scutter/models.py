import related
import os


@related.immutable()
class ExtractedLink(object):
    to_url = related.StringField(required=False)
    prior_text = related.StringField(required=False)
    link_text = related.StringField(required=False)
    after_text = related.StringField(required=False)
    headers = related.SequenceField(str, required=False, repr=True)
    anchor_text = related.StringField(required=False)
    from_url = related.StringField(required=False)

    def is_valid(self):
        return self.to_url and self.link_text


@related.immutable()
class ExtractedPage(object):
    # core
    url = related.StringField()
    title = related.StringField(required=False)

    # meta
    author = related.StringField(required=False)
    keywords = related.SequenceField(str, required=False)
    description = related.StringField(required=False)

    # twitter
    twitter_site = related.StringField(required=False)
    twitter_creator = related.StringField(required=False)
    twitter_image = related.StringField(required=False)
    twitter_description = related.StringField(required=False)

    # open graph
    og_type = related.StringField(required=False)
    og_image = related.StringField(required=False)
    og_description = related.StringField(required=False)

    # plain text content
    content = related.StringField(required=False, cmp=False, repr=False)


@related.immutable()
class Site(object):
    domain = related.StringField()
    non_canonical_params = related.SequenceField(str, required=False)
    seeds = related.SequenceField(str, required=False)
    follow = related.SequenceField(str, required=False)


@related.immutable()
class Config(object):
    sites = related.MappingField(Site, "domain")

    def __iter__(self):
        return iter(self.sites.items())

    def __getitem__(self, item):
        return self.sites[item]


file_path = os.path.join(os.path.dirname(__file__), "config/sites.yaml")
fp = open(file_path)
config = related.from_yaml(fp, Config)
