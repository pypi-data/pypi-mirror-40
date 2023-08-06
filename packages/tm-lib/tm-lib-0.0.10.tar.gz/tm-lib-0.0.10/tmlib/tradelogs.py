from mongoengine import ValidationError

from tmlib.models import TradeLog


def get_trade_logs(ticket=None):
    """
    Get trade logs by ticket ID;
    Return all the logs if no ticket id is specified
    :param ticket:
    :return:
    """
    mongo_filter = {}
    if ticket:
        mongo_filter['ticket'] = ticket
    trade_logs: TradeLog = TradeLog.objects_without_id(**mongo_filter)
    return [t.to_mongo() for t in trade_logs], 200


def put_trade_logs(tradelogs_body):
    """
    Add a new trade log.
    :param tradelogs_body:
    :return:
    """
    trade_log = TradeLog(**tradelogs_body)
    try:
        trade_log.save()
    except ValidationError as e:
        status = 400
        res = {
            "detail": e.message,
            "status": status,
            "title": "Bad Request",
            "type": "about:blank"
        }
        return res, status
    return trade_log.to_dict(), 201
