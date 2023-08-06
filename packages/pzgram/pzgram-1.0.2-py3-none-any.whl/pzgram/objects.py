import os
from typing import Union, TYPE_CHECKING

from .parsing import message_types, parse_forward_reply
from .useful import *
from .media_objects import *

if TYPE_CHECKING:
    from .bot import Bot


class Message:

    attributes = ["id", "sender", "date", "chat", "args",
                  "forward_from", "forward_from_chat", "forward_from_message_id", "forward_from_signature",
                  "reply_to_message", "edit_date", "media_group_id", "author_signature",
                  "text", "entities", "caption_entities", "audio", "document", "game", "photo", "sticker", "video",
                  "voice", "video_note", "caption", "contact", "location", "venue",
                  "new_chat_members", "left_chat_member", "new_chat_title", "new_chat_photo", "delete_chat_photo",
                  "group_chat_created", "supergroup_chat_created", "channel_chat_created", "migrate_from_chat_id",
                  "migrate_to_chat_id", "pinned_message"]

    def __init__(self, bot: "Bot", id: int, message_dict: Union[int, "Chat", dict]):
        self.bot = bot
        if isinstance(message_dict, dict) and len(message_dict):
            # If is a dict, parse as usual
            # Find the type of this message
            for t in message_types:
                if t in message_dict:
                    self.type = t
                    # Call the connected method for parsing that type of message
                    message_dict = message_types[t](message_dict, bot)
                    break
            # Parse other things
            message_dict = parse_forward_reply(message_dict, bot)
            # Add all possbile attributes to message_dict and set to None
            for i in self.attributes:
                if i not in message_dict:
                    message_dict[i] = None
            # Delete attribute from and replace with sender
            if "from" in message_dict:
                message_dict["sender"] = User(bot, message_dict["from"]["id"], message_dict["from"])
                message_dict.pop("from")
            message_dict["chat"] = Chat(bot, message_dict["chat"]["id"], message_dict["chat"])
        elif isinstance(message_dict, Chat):
            # if is a Chat Object
            chat = message_dict
            message_dict = {"chat": chat}
        elif isinstance(message_dict, int):
            # if is an Int, create Chat Object
            chat_id = message_dict
            message_dict = {"chat": Chat(self.bot, chat_id)}
        # Set Message ID
        message_dict["id"] = id
        # Memorize all attributes
        for i in message_dict:
            setattr(self, i, message_dict[i])

    def __str__(self) -> str:
        return "MessageObject{Type:" + self.type + " From:" + str(self.chat.id) + "}"

    def __repr__(self) -> str:
        return "MessageObject" + str(self.id)

    def forward(self, chat_id: Union[int, str], notification: bool=True) -> "Message":
        param = {
            "chat_id": chat_id,
            "from_chat_id": self.chat.id,
            "message_id": self.id,
            "disable_notification": not notification
        }
        r = api_request(self.bot, "forwardMessage", param=param)
        return Message(self.bot, r["message_id"], r)

    def delete(self) -> bool:
        param = {
            "chat_id": self.chat.id,
            "message_id": self.id
        }
        return api_request(self.bot, "deleteMessage", param=param)

    def edit(self, text: str, parse_mode: str=None, preview: bool=None, reply_markup: str=None) \
            -> Union[bool, "Message"]:
        p = {
            "chat_id": self.chat.id,
            "message_id": self.id,
            "text": text,
            "parse_mode": parse_mode,
            "disable_web_page_preview": preview,
            "reply_markup": reply_markup
        }
        r = api_request(self.bot, "editMessageText", p)
        # Check if the response is True or Message object
        if r == True:
            return True
        else:
            return Message(self.bot, r["message_id"], r)

    def edit_caption(self, caption: str, parse_mode: str=None, reply_markup: str=None) -> Union[bool, "Message"]:
        p = {
            "chat_id": self.chat.id,
            "message_id": self.id,
            "caption": caption,
            "parse_mode": parse_mode,
            "reply_markup": reply_markup
        }
        r = api_request(self.bot, "editMessageCaption", p)
        # Check if the response is True or Message object
        if r == True:
            return True
        else:
            return Message(self.bot, r["message_id"], r)

    def edit_reply_markup(self, reply_markup: str) -> Union[bool, "Message"]:
        p = {
            "chat_id": self.chat.id,
            "message_id": self.id,
            "reply_markup": reply_markup
        }
        r = api_request(self.bot, "editMessageReplyMarkup", p)
        # Check if the response is True or Message object
        if r == True:
            return True
        else:
            return Message(self.bot, r["message_id"], r)

    def edit_live(self, latitude: Union[int, float], longitude: Union[int, float], reply_markup: str=None) \
            -> Union[bool, "Message"]:
        p = {
            "chat_id": self.chat.id,
            "message_id": self.id,
            "latitude": latitude,
            "longitude": longitude,
            "reply_markup": reply_markup
        }
        r = api_request(self.bot, "editMessageLiveLocation", p)
        # Check if the response is True or Message object
        if r == True:
            return True
        else:
            return Message(self.bot, r["message_id"], r)

    def stop_live(self, reply_markup: str=None) -> Union[bool, "Message"]:
        p = {
            "chat_id": self.chat.id,
            "message_id": self.id,
            "reply_markup": reply_markup
        }
        r = api_request(self.bot, "stopMessageLiveLocation", p)
        if r == True:
            return True
        else:
            return Message(self.bot, r["message_id"], r)

    def reply(self, text: str, **kwargs) -> "Message":
        return self.chat.send(text, reply_to=self.id, **kwargs)

    def reply_photo(self, photopath: Union[Photo, str], **kwargs) -> "Message":
        return self.chat.send_photo(photopath, reply_id=self.id, **kwargs)

    def reply_voice(self, voicepath: Union[Voice, str], **kwargs) -> "Message":
        return self.chat.send_voice(voicepath, reply_id=self.id, **kwargs)

    def reply_audio(self, audiopath: Union[Audio, str], **kwargs) -> "Message":
        return self.chat.send_audio(audiopath, reply_id=self.id, **kwargs)

    def reply_document(self, documentpath: Union[Document, str], **kwargs) -> "Message":
        return self.chat.send_document(documentpath, reply_id=self.id, **kwargs)

    def reply_video(self, videopath: Union[Video, str], **kwargs) -> "Message":
        return self.chat.send_video(videopath, reply_id=self.id, **kwargs)

    def reply_videonote(self, videonotepath: Union[VideoNote, str], **kwargs) -> "Message":
        return self.chat.send_videonote(videonotepath, reply_id=self.id, **kwargs)

    def reply_sticker(self, stickerpath: Union[Sticker, str], **kwargs) -> "Message":
        return self.chat.send_sticker(stickerpath, reply_id=self.id, **kwargs)

    def reply_contact(self, phone_number: Union[Contact, str], *args, **kwargs) -> "Message":
        return self.chat.send_contact(phone_number, *args, reply_id=self.id, **kwargs)

    def reply_location(self, latitude: Union[int, float], longitude: Union[int, float], **kwargs) -> "Message":
        return self.chat.send_location(latitude, longitude, reply_id=self.id, **kwargs)

    def reply_venue(self, latitude: Union[Venue, float, int], *args, **kwargs) -> "Message":
        return self.chat.send_venue(latitude, *args, reply_id=self.id, **kwargs)


class Chat:

    attributes = ["id", "type", "title", "username", "first_name", "last_name", "all_members_are_administrator",
                  "photo", "description", "invite_link", "pinned_message", "sticker_set_name", "can_set_sticker_set"]

    def __init__(self, bot: "Bot", id: Union[int, str], chat_dict: dict=dict()):
        self.bot = bot
        chat_dict["id"] = id
        # For all attributes, check if is in the dict, otherwise set to None
        for i in self.attributes:
            if i in chat_dict:
                setattr(self, i, chat_dict[i])
            else:
                setattr(self, i, None)
        # Parse pinned_message and photo if they are not None (only returned in getChat)
        if self.pinned_message is not None:
            self.pinned_message = Message(bot, self.pinned_message["message_id"], self.pinned_message)
        if self.photo is not None:
            # Translate 2 file_id to 2 PhotoObject
            small_photo_dict = {"file_id": self.photo["small_file_id"], "width": 160, "height": 160}
            big_photo_dict = {"file_id": self.photo["big_file_id"], "width": 640, "height": 640}
            self.photo = [Photo(self.bot, small_photo_dict), Photo(self.bot, big_photo_dict)]

    def __str__(self) -> str:
        if self.type == "private":
            m = "Name:" + self.first_name
        else:
            m = "Title:" + self.title
        return "ChatObject{Id:" + str(self.id) + " " + m + "}"

    def __repr__(self) -> str:
        return "ChatObject" + str(self.id)

    def get_info(self) -> "Chat":
        p = {"chat_id": self.id}
        chat = api_request(self.bot, "getChat", p)
        return Chat(self.bot, chat["id"], chat)

    def send(self, text: str, parse_mode: str="", preview: bool=True, notification: bool=True,
             reply_id: Union[str, int] = None, reply_markup: str=None) -> Message:
        param = {
            "chat_id": self.id,
            "text": text,
            "parse_mode": parse_mode,
            "disable_web_page_preview": not preview,
            "disable_notification": notification,
            "reply_to_message_id": reply_id,
            "reply_markup": reply_markup
        }
        r = api_request(self.bot, "sendMessage", param)
        return Message(self.bot, r["message_id"], r)

    def forward_message(self, message_id: Union[str, int], chat_id: Union[str, int], notification: bool=True) \
            -> Message:
        param = {
            "chat_id": chat_id,
            "from_chat_id": self.id,
            "message_id": message_id,
            "disable_notification": not notification
        }
        r = api_request(self.bot, "forwardMessage", param=param)
        return Message(self.bot, r["message_id"], r)

    def delete_message(self, message_id: Union[str, int]) -> bool:
        param = {
            "chat_id": self.id,
            "message_id": message_id
        }
        return api_request(self.bot, "deleteMessage", param=param)

    def edit_message(self, message_id: Union[str, int], text: str, parse_mode: str=None, preview: bool=None,
                     reply_markup: str=None) -> Union[bool, Message]:
        p = {
            "chat_id": self.id,
            "message_id": message_id,
            "text": text,
            "parse_mode": parse_mode,
            "disable_web_page_preview": preview,
            "reply_markup": reply_markup
        }
        r = api_request(self.bot, "editMessageText", p)
        # Check if the response is True or Message object
        if r == True:
            return True
        else:
            return Message(self.bot, r["message_id"], r)

    def send_action(self, action: str) -> bool:
        param = {"chat_id": self.id, "action": action}
        return api_request(self.bot, "sendChatAction", param)

    def send_photo(self, photo: Union[str, Photo], caption: str=None, parse_mode: str=None, notification: bool=True,
                   reply_id: Union[int, str]=None, reply_markup: str=None) -> Message:
        if isinstance(photo, Photo):
            param = {
                "chat_id": self.id,
                "photo": photo.file_id,
                "caption": caption,
                "parse_mode": parse_mode,
                "disable_notification": not notification,
                "reply_to_message_id": reply_id,
                "reply_markup": reply_markup
            }
            r = api_request(self.bot, "sendPhoto", param)
            return Message(self.bot, r["message_id"], r)
        else:
            # Check if file exists
            if not os.path.isfile(photo):
                raise FileNotFoundError("File " + photo + " not exists or is a folder")
            # Find the name of that file from his path
            name = file_name(photo)
            file = {
                "photo": (name, open(photo, "rb"))
            }
            param = {
                "chat_id": self.id,
                "caption": caption,
                "parse_mode": parse_mode,
                "disable_notification": not notification,
                "reply_to_message_id": reply_id,
                "reply_markup": reply_markup
            }
            r = api_request(self.bot, "sendPhoto", param, file)
            return Message(self.bot, r["message_id"], r)

    def send_voice(self, voice: Union[Voice, str], duration: int=None, caption: str=None, 
                   parse_mode: str=None, notification: bool=True, reply_id: Union[str, int]=None, 
                   reply_markup: str=None) -> Message:
        if isinstance(voice, Voice):
            param = {
                "chat_id": self.id,
                "voice": voice.file_id,
                "duration": voice.duration,
                "caption": caption,
                "parse_mode": parse_mode,
                "disable_notification": not notification,
                "reply_to_message_id": reply_id,
                "reply_markup": reply_markup
            }
            r = api_request(self.bot, "sendVoice", param)
            return Message(self.bot, r["message_id"], r)
        else:
            # Check if file exists
            if not os.path.isfile(voice):
                raise FileNotFoundError("File " + voice + " not exists or is a folder")
            # Find the name of that file from his path
            name = file_name(voice)
            file = {
                "voice": (name, open(voice, "rb"))
            }
            param = {
                "chat_id": self.id,
                "duration": duration,
                "caption": caption,
                "parse_mode": parse_mode,
                "disable_notification": not notification,
                "reply_to_message_id": reply_id,
                "reply_markup": reply_markup
            }
            r = api_request(self.bot, "sendVoice", param, file)
            return Message(self.bot, r["message_id"], r)

    def send_audio(self, audio: Union[Audio, str], duration: int=None, performer: str=None, 
                   title: str=None, caption: str=None, parse_mode: str=None, notification: bool=True, 
                   reply_id: Union[int, str]=None, reply_markup: str=None) -> Message:
        if isinstance(audio, Audio):
            param = {
                "chat_id": self.id,
                "audio": audio.file_id,
                "duration": audio.duration,
                "performer": audio.performer,
                "title": audio.title,
                "caption": caption,
                "parse_mode": parse_mode,
                "disable_notification": not notification,
                "reply_to_message_id": reply_id,
                "reply_markup": reply_markup
            }
            r = api_request(self.bot, "sendAudio", param)
            return Message(self.bot, r["message_id"], r)
        else:
            # Check if file exists
            if not os.path.isfile(audio):
                raise FileNotFoundError("File " + audio + " not exists or is a folder")
            # Find the name of that file from his path
            name = file_name(audio)
            file = {
                "audio": (name, open(audio, "rb"))
            }
            param = {
                "chat_id": self.id,
                "duration": duration,
                "performer": performer,
                "title": title,
                "caption": caption,
                "parse_mode": parse_mode,
                "disable_notification": not notification,
                "reply_to_message_id": reply_id,
                "reply_markup": reply_markup
            }
            r = api_request(self.bot, "sendAudio", param, file)
            return Message(self.bot, r["message_id"], r)

    def send_document(self, document: Union[Document, str], caption: str=None, parse_mode: str=None, 
                      notification: bool=True, reply_id: Union[int, str]=None, reply_markup: str=None) -> Message:
        if isinstance(document, Document):
            param = {
                "chat_id": self.id,
                "document": document.file_id,
                "caption": caption,
                "parse_mode": parse_mode,
                "disable_notification": not notification,
                "reply_to_message_id": reply_id,
                "reply_markup": reply_markup
            }
            r = api_request(self.bot, "sendDocument", param)
            return Message(self.bot, r["message_id"], r)
        else:
            # Check if file exists
            if not os.path.isfile(document):
                raise FileNotFoundError("File " + document + " not exists or is a folder")
            # Find the name of that file from his path
            name = file_name(document)
            file = {
                "document": (name, open(document, "rb"))
            }
            param = {
                "chat_id": self.id,
                "caption": caption,
                "parse_mode": parse_mode,
                "disable_notification": not notification,
                "reply_to_message_id": reply_id,
                "reply_markup": reply_markup
            }
            r = api_request(self.bot, "sendDocument", param, file)
            return Message(self.bot, r["message_id"], r)

    def send_video(self, video: Union[Voice, str], duration: int=None, width: int=None, height: int=None,
                   caption: str=None, parse_mode: str=None, support_streaming: bool=None, notification: bool=True, 
                   reply_id: Union[int, str]=None, reply_markup: str=None) -> Message:
        if isinstance(video, Video):
            param = {
                "chat_id": self.id,
                "video": video,
                "duration": video.duration,
                "width": video.width,
                "height": video.height,
                "caption": caption,
                "parse_mode": parse_mode,
                "support_straming": support_streaming,
                "disable_notification": not notification,
                "reply_to_message_id": reply_id,
                "reply_markup": reply_markup
            }
            r = api_request(self.bot, "sendVideo", param)
            return Message(self.bot, r["message_id"], r)
        else:
            # Check if file exists
            if not os.path.isfile(video):
                raise FileNotFoundError("File " + video + " not exists or is a folder")
            # Find the name of that file from his path
            name = file_name(video)
            file = {
                "video": (name, open(video, "rb"))
            }
            param = {
                "chat_id": self.id,
                "duration": duration,
                "width": width,
                "height": height,
                "caption": caption,
                "parse_mode": parse_mode,
                "support_straming": support_streaming,
                "disable_notification": not notification,
                "reply_to_message_id": reply_id,
                "reply_markup": reply_markup
            }
            r = api_request(self.bot, "sendVideo", param, file)
            return Message(self.bot, r["message_id"], r)

    def send_videonote(self, videonote: Union[VideoNote, str], duration: int=None, length: int=None,
                       notification: bool=True, reply_id: Union[int, str]=None, reply_markup: dict=None) -> Message:
        if isinstance(videonote, VideoNote):
            param = {
                "chat_id": self.id,
                "video_note": videonote.file_id,
                "duration": videonote.duration,
                "length": videonote.length,
                "disable_notification": not notification,
                "reply_to_message_id": reply_id,
                "reply_markup": reply_markup
            }
            r = api_request(self.bot, "sendVideoNote", param)
            return Message(self.bot, r["message_id"], r)
        else:
            # Check if file exists
            if not os.path.isfile(videonote):
                raise FileNotFoundError("File " + videonote + " not exists or is a folder")
            # Find the name of that file from his path
            name = file_name(videonote)
            file = {
                "video_note": (name, open(videonote, "rb"))
            }
            param = {
                "chat_id": self.id,
                "duration": duration,
                "length": length,
                "disable_notification": not notification,
                "reply_to_message_id": reply_id,
                "reply_markup": reply_markup
            }
            r = api_request(self.bot, "sendVideoNote", param, file)
            return Message(self.bot, r["message_id"], r)

    def send_sticker(self, sticker: Union[Sticker, str], notification: bool=True, reply_id: Union[int, str]=None,
                     reply_markup: dict=None) -> Message:
        if isinstance(sticker, Sticker):
            param = {
                "chat_id": self.id,
                "sticker": sticker.file_id,
                "disable_notification": not notification,
                "reply_to_message_id": reply_id,
                "reply_markup": reply_markup
            }
            r = api_request(self.bot, "sendSticker", param)
            return Message(self.bot, r["message_id"], r)
        else:
            # Check if file exists
            if not os.path.isfile(sticker):
                raise FileNotFoundError("File " + sticker + " not exists or is a folder")
            # Find the name of that file from his path
            name = file_name(sticker)
            file = {
                "sticker": (name, open(sticker, "rb"))
            }
            param = {
                "chat_id": self.id,
                "disable_notification": not notification,
                "reply_to_message_id": reply_id,
                "reply_markup": reply_markup
            }
            r = api_request(self.bot, "sendSticker", param, file)
            return Message(self.bot, r["message_id"], r)

    def send_contact(self, phone_number: Union[Contact, str], first_name: str=None, last_name: str=None,
                     user_id: Union[int, str]=None, notification: bool=True, reply_id: Union[int, str]=None,
                     reply_markup: dict=None) -> Message:
        if isinstance(phone_number, Contact):
            contact = phone_number
            param = {
                "chat_id": self.id,
                "phone_number": contact.phone_number,
                "first_name": contact.first_name,
                "last_name": contact.last_name,
                "user_id": contact.user_id,
                "disable_notification": not notification,
                "reply_to_message_id": reply_id,
                "reply_markup": reply_markup
            }
            r = api_request(self.bot, "sendContact", param)
            return Message(self.bot, r["message_id"], r)
        else:
            param = {
                "chat_id": self.id,
                "phone_number": phone_number,
                "first_name": first_name,
                "last_name": last_name,
                "user_id": user_id,
                "disable_notification": not notification,
                "reply_to_message_id": reply_id,
                "reply_markup": reply_markup
            }
            r = api_request(self.bot, "sendContact", param)
            return Message(self.bot, r["message_id"], r)

    def send_location(self, latitude: Union[int, float], longitude: Union[int, float], live_period: int=None,
                      notification: bool=True, reply_id: Union[int, str]=None, reply_markup: dict=None) -> Message:
        param = {
            "chat_id": self.id,
            "latitude": latitude,
            "longitude": longitude,
            "live_period": live_period,
            "disable_notification": not notification,
            "reply_to_message_id": reply_id,
            "reply_markup": reply_markup
        }
        r = api_request(self.bot, "sendLocation", param)
        return Message(self.bot, r["message_id"], r)

    def send_venue(self, latitude: Union[Venue, float, int], longitude: Union[float, int]=None, title: str=None,
                   address: str=None, foursquare_id: str=None, notification: bool=True, reply_id: Union[int, str]=None,
                   reply_markup: dict=None) -> Message:
        if isinstance(latitude, Venue):
            venue = latitude
            param = {
                "chat_id": self.id,
                "latitude": venue.location.latitude,
                "longitude": venue.location.longitude,
                "title": venue.title,
                "address": venue.address,
                "foursquare_id": venue.foursquare_id,
                "disable_notification": not notification,
                "reply_to_message_id": reply_id,
                "reply_markup": reply_markup
            }
            r = api_request(self.bot, "sendVenue", param)
            return Message(self.bot, r["message_id"], r)
        else:
            param = {
                "chat_id": self.id,
                "latitude": latitude,
                "longitude": longitude,
                "title": title,
                "address": address,
                "foursquare_id": foursquare_id,
                "disable_notification": not notification,
                "reply_to_message_id": reply_id,
                "reply_markup": reply_markup
            }
            r = api_request(self.bot, "sendVenue", param)
            return Message(self.bot, r["message_id"], r)

    def kick_user(self, user_id: Union[int, str], until_date: int=None) -> bool:
        if self.type == "private":
            raise WrongChatTypeError("You can't kick someone from a private Chat")
        p = {
            "chat_id": self.id,
            "user_id": user_id,
            "until_date": until_date
        }
        return api_request(self.bot, "kickChatMember", p)

    def unban_user(self, user_id: Union[int, str]) -> bool:
        if self.type == "private":
            raise WrongChatTypeError("You can't unban someone from a private Chat")
        p = {"chat_id": self.id, "user_id": user_id}
        return api_request(self.bot, "unbanChatMember")

    def restrict_user(self, user_id: Union[int, str], until_date: int=None, send_message: bool=None,
                      send_media: bool=None, send_other: bool=None, web_page_preview: bool=None) -> bool:
        if self.type != "supergroup":
            raise WrongChatTypeError("RestrictUser can only be used in supergroups")
        p = {
            "chat_id": self.id,
            "user_id": user_id,
            "until_date": until_date,
            "can_send_messages": send_message,
            "can_send_media_messages": send_media,
            "can_send_other_messages": send_other,
            "can_add_web_page_previews": web_page_preview
        }
        return api_request(self.bot, "restrictChatMember", p)

    def promote_user(self, user_id: Union[int, str], change_info: bool=None, post_message: bool=None,
                     edit_message: bool=None, delete_message: bool=None, invite_user: bool=None,
                     restrict_user: bool=None, pin_message: bool=None, promote_user: bool=None) -> bool:
        if self.type != "supergroup" and self.type != "channel":
            raise WrongChatTypeError("PromoteUser can only be used in supergroups or channels")
        p = {
            "chat_id": self.id,
            "user_id": user_id,
            "can_change_info": change_info,
            "can_post_messages": post_message,
            "can_edit_messages": edit_message,
            "can_delete_message": delete_message,
            "can_invite_users": invite_user,
            "can_restrict_users": restrict_user,
            "can_pin_messages": pin_message,
            "can_promote_users": promote_user
        }
        return api_request(self.bot, "promoteChatMember", p)

    def new_invite_link(self) -> str:
        return api_request(self.bot, "exportChatInviteLink", {"chat_id": self.id})

    def set_photo(self, photopath: str) -> bool:
        # Check if file exists
        if not os.path.isfile(photopath):
            raise FileNotFoundError("File " + photopath + " not exists or is a folder")
        # Find the name of that file from his path
        name = file_name(photopath)
        file = {
            "photo": (name, open(photopath, "rb"))
        }
        return api_request(self.bot, "setChatPhoto", {"chat_id": self.id}, file)

    def delete_photo(self) -> bool:
        if self.type == "private":
            raise WrongChatTypeError("DeleteChatPhoto can only be used in groups or channels")
        return api_request(self.bot, "deleteChatPhoto", {"chat_id": self.id})

    def set_title(self, title: str) -> bool:
        if self.type == "private":
            raise WrongChatTypeError("SetChatTitle can only be used in groups or channels")
        return api_request(self.bot, "setChatTitle", {"chat_id": self.id, "title": title})

    def set_description(self, description: str) -> bool:
        if self.type == "private" or self.type == "group":
            raise WrongChatTypeError("SetChatDescription can only be used in supergroups or channels")
        return api_request(self.bot, "setChatDescription", {"chat_id": self.id, "description": description})

    def pin_message(self, message_id: Union[int, str], notification: bool=True) -> bool:
        if self.type == "private" or self.type == "group":
            raise WrongChatTypeError("PinMessage can only be used in supergroups or channels")
        p = {
            "chat_id": self.id,
            "message_id": message_id,
            "disable_notification": not notification
        }
        return api_request(self.bot, "pinChatMessage", p)

    def unpin_message(self) -> bool:
        if self.type == "private" or self.type == "group":
            raise WrongChatTypeError("unPinMessage can only be used in supergroups or channels")
        return api_request(self.bot, "unpinChatMessage", {"chat_id": self.id})

    def leave(self) -> bool:
        if self.type == "private":
            raise WrongChatTypeError("LeaveChat can only be used in groups or channels")
        return api_request(self.bot, "leaveChat", {"chat_id": self.id})

    def get_admins(self) -> list:
        if self.type == "private":
            raise WrongChatTypeError("LeaveChat can only be used in groups or channels")
        # Return a list of ChatMember objects, each rappresenting a single admin
        users = api_request(self.bot, "getChatAdministrators", {"chat_id": self.id})
        admins = []
        for u in users:
            admins.append(ChatMember(self.bot, u))
        return admins

    def get_members_count(self) -> int:
        if self.type == "private":
            raise WrongChatTypeError("LeaveChat can only be used in groups or channels")
        return api_request(self.bot, "getChatMembersCount", {"chat_id": self.id})

    def get_member(self, user_id) -> "ChatMember":
        if self.type == "private":
            raise WrongChatTypeError("LeaveChat can only be used in groups or channels")
        return ChatMember(self.bot, api_request(self.bot, "getChatMember", {"chat_id": self.id, "user_id": user_id}))


class User:

    attirbutes = ["id", "is_bot", "first_name", "last_name", "username", "language_code"]

    def __init__(self, bot: "Bot", id: Union[int, str], user_dict: dict=dict()):
        self.bot = bot
        user_dict["id"] = id
        # For all attributes, check if is in the dict, otherwise set to None
        for i in self.attirbutes:
            if i in user_dict:
                setattr(self, i, user_dict[i])
            else:
                setattr(self, i, None)

    def __str__(self) -> str:
        if self.is_bot:
            return "UserObject{Id:" + str(self.id) + " Name:" + self.first_name + " IsBot: True}"
        else:
            return "UserObject{Id:" + str(self.id) + " Name:" + self.first_name + "}"

    def __repr__(self) -> str:
        return "UserObject" + str(self.id)

    def get_profile_photos(self, offset: int=None, limit: int=None) -> list:
        # Offset from the first, default send the last 100 profile photos
        p = {
            "user_id": self.id,
            "offset": offset,
            "limit": limit
        }
        photos_dict = api_request(self.bot, "getUserProfilePhotos", p)
        # List of List of PhotoSize (Each photo has more sizes)
        photos = []
        for i in photos_dict["photos"]:
            # For each Photo
            photo = []
            for j in i:
                # For each size
                photo.append(Photo(self.bot, j))
            photos.append(photo)
        return photos

    def send(self, text: str, **kwargs) -> Message:
        return Chat(self.bot, self.id).send(text, **kwargs)

    def send_photo(self, photopath: Union[Photo, str], **kwargs) -> Message:
        return Chat(self.bot, self.id).send_photo(photopath, **kwargs)

    def send_voice(self, voicepath: Union[Voice, str], **kwargs) -> Message:
        return Chat(self.bot, self.id).send_voice(voicepath, **kwargs)

    def send_audio(self, audiopath: Union[Audio, str], **kwargs) -> Message:
        return Chat(self.bot, self.id).send_audio(audiopath, **kwargs)

    def send_document(self, documentpath: [Document, str], **kwargs) -> Message:
        return Chat(self.bot, self.id).send_document(documentpath, **kwargs)

    def send_video(self, videopath: [Video, str], **kwargs) -> Message:
        return Chat(self.bot, self.id).send_video(videopath, **kwargs)

    def send_videonote(self, videonotepath: Union[VideoNote, str], **kwargs) -> Message:
        return Chat(self.bot, self.id).send_videonote(videonotepath, **kwargs)

    def send_sticker(self, stickerpath: Union[Sticker, str], **kwargs) -> Message:
        return Chat(self.bot, self.id).send_sticker(stickerpath, **kwargs)

    def send_contact(self, phone_number: Union[Contact, str], *args, **kwargs) -> Message:
        return Chat(self.bot, self.id).send_contact(phone_number, *args, **kwargs)

    def send_location(self, latitude: Union[float, int], longitude: Union[float, int], **kwargs) -> Message:
        return Chat(self.bot, self.id).send_location(latitude, longitude, **kwargs)

    def send_venue(self, latitude: Union[Venue, float, int], *args, **kwargs) -> Message:
        return Chat(self.bot, self.id).send_venue(latitude, *args, **kwargs)


class ChatMember(User):

    attributes = ["status", "until_date", "can_be_edited", "can_change_info", "can_post_messages", "can_edit_messages",
                  "can_delete_messages", "can_invite_users", "can_restrict_members", "can_pin_messages",
                  "can_promote_members", "can_send_messages", "can_send_media_messages", "can_add_web_page_previews"]

    def __init__(self, bot: "Bot", user_dict: dict):
        # Call the User init, and after, set the attributes of a ChatMember
        User.__init__(self, bot, user_dict["user"]["id"], user_dict["user"])
        user_dict.pop("user", None)
        for i in self.attirbutes:
            if i in user_dict:
                setattr(self, i, user_dict[i])
            else:
                setattr(self, i, None)

    def __str__(self) -> str:
        return "ChatMemberObject" + str(self.id)
