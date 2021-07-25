private void sendMessage(String body, String toJid) {
     try {
         Jid jid = JidCreate.from(toJid + "@" + MyApplication.CHAT_DOMAIN);
         Chat chat = ChatManager.getInstanceFor(mConnection)
                 .createChat(jid.asJidWithLocalpartIfPossible());
         chat.sendMessage(body);
     } catch (Exception e) {
     } 
}