from lxml import etree

from grow_recipe import constants, check_for_error


class Metric:

    def __init__(self, min_value=None, max_value=None):
        self.min = min_value
        if self.min:
            self.min = float(self.min)

        self.max = max_value
        if self.max:
            self.max = float(self.max)


def find_metric_value(xml, stage, topic, metric):
    """
    Takes in a buffer, xml,  and finds the specified metric in the
    given stage. If the metric is not present in the given stage,
    the metric is taken from the default stage
    """

    # put the buffer back to the beginning
    xml.seek(0)

    # raise schema errors if they exist
    check_for_error(xml)

    xml.seek(0)

    tree = etree.parse(xml)

    if not stage:
        stage = constants.DEFAULT

    value = tree.xpath('/{root}/{stage}/{topic}/{metric}'
                       .format(root=constants.ROOT_NODE, stage=stage,
                               topic=topic, metric=metric))

    if not value:
        value = tree.xpath('/{root}/{stage}/{topic}/{metric}'.format(
            root=constants.ROOT_NODE,
            stage=constants.DEFAULT,
            topic=topic,
            metric=metric
        ))

    if not value:
        return None

    # there should only be definition if the metric is present
    assert len(value) == 1

    return Metric(value[0].attrib.get('min'),
                  value[0].attrib.get('max'))
